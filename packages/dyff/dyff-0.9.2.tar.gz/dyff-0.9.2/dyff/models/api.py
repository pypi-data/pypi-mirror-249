# Copyright UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
import contextlib
import importlib
import importlib.resources

# FIXME: All this stuff is for a temporary workaround for a BentoML 1.1 issue.
# See: https://github.com/bentoml/BentoML/issues/4080
import os
import re
import string
import subprocess
import tarfile
import tempfile
import typing
from pathlib import Path
from typing import Any, Dict, NamedTuple, Optional

import bentoml
import smart_open
import yaml
from bentoml._internal.bento import Bento
from bentoml._internal.configuration.containers import BentoMLContainer
from bentoml._internal.utils import resolve_user_filepath
from bentoml.exceptions import InvalidArgument
from simple_di import Provide, inject

import dyff.models.sources

from ..core import dynamic_import
from ..schema.models.tasks import AnyTask
from ..schema.platform import ModelSource
from .outputs import OutputSpecification

if typing.TYPE_CHECKING:
    from bentoml._internal.bento import BentoStore
#     from bentoml._internal.bento.build_config import CondaOptions
#     from bentoml._internal.bento.build_config import DockerOptions
#     from bentoml._internal.bento.build_config import ModelSpec
#     from bentoml._internal.bento.build_config import PythonOptions
#     from bentoml._internal.cloud import BentoCloudClient
#     from bentoml.server import Server


class BentoBuildSpec(NamedTuple):
    input_descriptor: str
    output_descriptor: str
    bentofile: Dict
    inference_kwargs: Optional[Dict] = None


class HTTPPayload(NamedTuple):
    headers: Dict[str, Any]
    data: Any


class ModelInterface:
    @abc.abstractproperty
    def output_spec(self) -> OutputSpecification:
        raise NotImplementedError()

    @abc.abstractproperty
    def inference_task(self) -> AnyTask:
        raise NotImplementedError()

    @abc.abstractmethod
    def _rpc_encode_input(self, item: Dict) -> HTTPPayload:
        """Framework-specific implementation of input encoding."""
        raise NotImplementedError()

    @abc.abstractmethod
    def _rpc_decode_output(self, item: Any) -> Dict[str, Any]:
        """Framework-specific implementation of output decoding."""
        raise NotImplementedError()

    @abc.abstractmethod
    def prepare_bento_model(self, local_path: str, model_tag: str) -> BentoBuildSpec:
        """Prepare the artifacts needed for building a Bento for this model.

        Parameters:
          local_path: A local filesystem directory where the model files are
            available.
          model_tag: The tag to use for the created Bento package.

        Returns:
          A BentoBuildSpec containing information about the Bento package.
        """
        raise NotImplementedError()

    def rpc_encode_input(self, item: Dict) -> HTTPPayload:
        """Encode a data item into an HTTP payload suitable for making an RPC
        call to the inference service.
        """
        return self._rpc_encode_input(item)

    def rpc_decode_output(self, index: int, item: Any) -> Any:
        """Decode the JSON-format RPC response into a Python dict matching the
        output schema. Raises a subclass of ``dyff.models.outputs.TaskOutputError``
        if the output is mal-formed.
        """
        result = self._rpc_decode_output(item)
        result["_index_"] = index
        self.output_spec.verify_output(result)
        return result


def get_model_interface(interface_type: str, inference_task: AnyTask) -> ModelInterface:
    """Create a ``ModelInterface`` instance appropriate for the model interface
    and inference task.
    """
    return dynamic_import.instantiate(
        f"dyff.models.frameworks.{interface_type}", inference_task
    )


def fetch(source: ModelSource, local_path: str):
    """Obtain the model files.

    Parameters:
      source: The specification of the source.
      local_path: Local filesystem path to fetch the files into.
    """
    impl = dyff.models.sources.create_source(source)
    impl.fetch(local_path)


@inject
def _build_bentofile_with_bentoml_home(
    bentofile: str = "bentofile.yaml",
    *,
    version: str | None = None,
    build_ctx: str | None = None,
    _bentoml_home: str = Provide[BentoMLContainer.bentoml_home],
    _bento_store: BentoStore = Provide[BentoMLContainer.bento_store],
) -> Bento:
    """
    This is a copy-paste of `bentoml.bentos.build_bentofile` modified to
    set the `BENTOML_HOME` environment variable in the subprocess call.

    FIXME: This is a temporary workaround for a BentoML 1.1 issue.
    See: https://github.com/bentoml/BentoML/issues/4080

    Build a Bento base on options specified in a bentofile.yaml file.

    By default, this function will look for a `bentofile.yaml` file in current working
    directory.

    Args:
        bentofile: The file path to build config yaml file
        version: Override the default auto generated version str
        build_ctx: Build context directory, when used as
        _bento_store: save Bento created to this BentoStore
    """
    try:
        bentofile = resolve_user_filepath(bentofile, build_ctx)
    except FileNotFoundError as ex:
        raise InvalidArgument(f'bentofile "{bentofile}" not found') from ex

    build_args = ["bentoml", "build"]
    if build_ctx is None:
        build_ctx = "."
    build_args.append(build_ctx)
    if version is not None:
        build_args.extend(["--version", version])
    build_args.extend(["--bentofile", bentofile, "--output", "tag"])
    env = os.environ.copy()
    env["BENTOML_HOME"] = _bentoml_home

    try:
        output = subprocess.check_output(build_args, env=env)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Failed to build BentoService bundle") from e

    pattern = r"^__tag__:[^:\n]+:[^:\n]+"
    matched = re.search(pattern, output.decode("utf-8").strip(), re.MULTILINE)
    assert matched is not None, f"Failed to find tag from output: {output}"
    _, _, tag = matched.group(0).partition(":")
    return bentoml.bentos.get(tag, _bento_store=_bento_store)


def create_bento(
    *,
    model_interface: ModelInterface,
    model_tag: str,
    service_name: str,
    input_path: str,
    output_path: str,
    scratch_dir: Optional[str] = None,
) -> bentoml.Bento:
    """Build a Bento package for the model from the prepared build artifacts."""

    def scratch_dir_context(scratch_dir=scratch_dir):
        if scratch_dir is not None:
            scratch_dir = Path(scratch_dir)
            return contextlib.nullcontext(scratch_dir)
        else:
            return tempfile.TemporaryDirectory("alignmentlabs")

    # "a tag's name or version must consist of alphanumeric characters, '_', '-', or '.'"
    def sanitize(s: str) -> str:
        return re.sub(r"[^A-Za-z0-9_\-.]", "-", s)

    model_tag = sanitize(model_tag)
    service_name = sanitize(service_name)

    # Temporarily change BENTOML_HOME to the scratch directory
    with scratch_dir_context() as tmp, bentoml.bentos.BentoMLContainer.bentoml_home.patch(
        tmp
    ):
        os.environ["BENTOML_HOME"] = str(tmp)
        tmp = Path(tmp)
        build = tmp / "build"
        build.mkdir(exist_ok=True)
        # BentoML expects these to exist already
        (tmp / "models").mkdir(exist_ok=True)
        (tmp / "bentos").mkdir(exist_ok=True)

        model_spec = model_interface.prepare_bento_model(input_path, model_tag)

        # Create service.py
        service_substitutions = {
            "model_tag": model_tag,
            "service_name": service_name,
            "input_descriptor": model_spec.input_descriptor,
            "output_descriptor": model_spec.output_descriptor,
            "inference_kwargs": "",  # Default value
        }
        if model_spec.inference_kwargs is not None:
            # Convert the kwargs dict into a string containing function arg syntax.
            # This gets appended to the arguments in the service template.
            tokens = []
            for k, v in model_spec.inference_kwargs.items():
                tokens.append(f", {k}={repr(v)}")
            service_substitutions["inference_kwargs"] = "".join(tokens)

        service_template = importlib.resources.read_text(
            "dyff.models.bentoml", "service.py-template"
        )
        service_definition = string.Template(service_template).substitute(
            service_substitutions
        )

        # Finish Bentofile boilerplate
        model_spec.bentofile["service"] = "service.py:service"
        model_spec.bentofile.setdefault("labels", {}).update(
            {"model_tag": model_tag, "service_name": service_name}
        )

        with open(build / "bentofile.yaml", "w") as fout:
            yaml.dump(model_spec.bentofile, fout)
        with open(build / "service.py", "w") as fout:
            fout.write(service_definition)
        # FIXME: There is an issue with BentoML 1.1 where config changes aren't
        # seen by the builder because it runs in a subprocess. We're replacing
        # their function with a very-slightly-modified copy-paste as a workaround.
        # See: https://github.com/bentoml/BentoML/issues/4080
        # bento = bentoml.bentos.build_bentofile(build_ctx=build)
        bento = _build_bentofile_with_bentoml_home(build_ctx=build)

        # Note: We're gzipping via tarfile, so we disable compression for
        # smart_open (which would otherwise infer it from .gz). It seems to work
        # without disabling compression, but we'll do it anyway just to be safe.
        # TODO: The 'source.tar.gz' name is specified in dyff.storage, but we
        # don't want the models package to depend on dyff.
        with smart_open.open(
            f"{output_path}/source.tar.gz",
            "wb",
            compression="disable",
            transport_params=dict(blob_open_kwargs=dict(timeout=1800)),
        ) as fout:
            with tarfile.open(fileobj=fout, mode="w|gz") as tar:
                # arcname="." because we want paths in the tar archive to be relative
                # to the bento root directory
                tar.add(bento.path, arcname=".", recursive=True)
        return bento
