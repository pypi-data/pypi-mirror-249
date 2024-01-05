# Copyright UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing as t
import warnings

import bentoml

# from bentoml._internal.configuration.containers import BentoMLContainer
import openllm
import openllm_core

if t.TYPE_CHECKING:
    from bentoml._internal.runner.runner import AbstractRunner

# The following warnings from bitsandbytes, and probably not that important for users to see
warnings.filterwarnings(
    "ignore",
    message="MatMul8bitLt: inputs will be cast from torch.float32 to float16 during quantization",
)
warnings.filterwarnings(
    "ignore",
    message="MatMul8bitLt: inputs will be cast from torch.bfloat16 to float16 during quantization",
)
warnings.filterwarnings(
    "ignore",
    message="The installed version of bitsandbytes was compiled without GPU support.",
)

# Try to increase the Runner timeout
# Relevant error:
# Exception on /v1/generate [POST] (trace=b3bf2bb8df28af20d82d62cb018b0781,span=abd51cc11f0d0a33,sampled=0,service.name=llm-dolly-v2-service)
# Traceback (most recent call last):
#   File "/usr/local/lib/python3.9/site-packages/bentoml/_internal/server/http_app.py", line 341, in api_func
#     output = await api.func(*args)
#   File "/dyff/mnt/model/bentos/databricks--dolly-v2-3b-service/f6c9be08f16fe4d3a719bee0a4a7c7415b5c65df/src/openllm_service.py", line 65, in generate_v1
#     responses = await runner.generate.async_run(
#   File "/usr/local/lib/python3.9/site-packages/bentoml/_internal/runner/runner.py", line 55, in async_run
#     return await self.runner._runner_handle.async_run_method(self, *args, **kwargs)
#   File "/usr/local/lib/python3.9/site-packages/bentoml/_internal/runner/runner_handle/remote.py", line 216, in async_run_method
#     async with self._client.post(
#   File "/usr/local/lib/python3.9/site-packages/aiohttp/client.py", line 1141, in __aenter__
#     self._resp = await self._coro
#   File "/usr/local/lib/python3.9/site-packages/aiohttp/client.py", line 560, in _request
#     await resp.start(conn)
#   File "/usr/local/lib/python3.9/site-packages/aiohttp/client_reqrep.py", line 914, in start
#     self._continue = None
#   File "/usr/local/lib/python3.9/site-packages/aiohttp/helpers.py", line 721, in __exit__
#     raise asyncio.TimeoutError from None
# asyncio.exceptions.TimeoutError
runners_config = bentoml.bentos.BentoMLContainer.runners_config.get()
traffic = runners_config.get("traffic", {})
traffic["timeout"] = 3_600_000
runners_config["traffic"] = traffic
bentoml.bentos.BentoMLContainer.runners_config.set(runners_config)

base_model_name = "${openllm_base_model}"
llm_config = openllm.AutoConfig.for_model(base_model_name)
runner = openllm.Runner(base_model_name, llm_config=llm_config, ensure_available=False)
runners: list[AbstractRunner] = [runner]

runners_config = bentoml.bentos.BentoMLContainer.runners_config.get()
if runner.name in runners_config:
    traffic = runners_config[runner.name].get("traffic", {})
    traffic["timeout"] = 3_600_000
    runners_config[runner.name]["traffic"] = traffic
    bentoml.bentos.BentoMLContainer.runners_config.set(runners_config)

svc = bentoml.Service(name=f"llm-{llm_config['start_name']}-service", runners=runners)

_JsonInput = bentoml.io.JSON.from_sample(
    {
        "prompt": "",
        "llm_config": llm_config.model_dump(flatten=True),
        "adapter_name": None,
    }
)


@svc.api(
    route="/v1/generate",
    input=_JsonInput,
    output=bentoml.io.JSON.from_sample(
        {"responses": [], "configuration": llm_config.model_dump(flatten=True)}
    ),
)
async def generate_v1(input_dict: dict[str, t.Any]) -> openllm.GenerationOutput:
    echo = input_dict.pop("echo", False)
    qa_inputs = openllm.GenerationInput.from_llm_config(llm_config)(**input_dict)
    config = qa_inputs.llm_config.model_dump()
    if runner.backend == "vllm":
        async for output in runner.vllm_generate.async_stream(
            qa_inputs.prompt,
            adapter_name=qa_inputs.adapter_name,
            echo=echo,
            request_id=openllm_core.utils.gen_random_uuid(),
            **config,
        ):
            responses = output
        if responses is None:
            raise ValueError("'responses' should not be None.")
    else:
        responses = await runner.generate.async_run(
            qa_inputs.prompt, adapter_name=qa_inputs.adapter_name, **config
        )
    return openllm.GenerationOutput(responses=responses, configuration=config)


@svc.api(
    route="/v1/generate_stream",
    input=_JsonInput,
    output=bentoml.io.Text(content_type="text/event-stream"),
)
async def generate_stream_v1(
    input_dict: dict[str, t.Any]
) -> t.AsyncGenerator[str, None]:
    echo = input_dict.pop("echo", False)
    qa_inputs = openllm.GenerationInput.from_llm_config(llm_config)(**input_dict)
    if runner.backend == "vllm":
        return runner.vllm_generate_iterator.async_stream(
            qa_inputs.prompt,
            adapter_name=qa_inputs.adapter_name,
            echo=echo,
            request_id=openllm_core.utils.gen_random_uuid(),
            **qa_inputs.llm_config.model_dump(),
        )
    else:
        return runner.generate_iterator.async_stream(
            qa_inputs.prompt,
            adapter_name=qa_inputs.adapter_name,
            echo=echo,
            **qa_inputs.llm_config.model_dump(),
        )


@svc.api(
    route="/v1/metadata",
    input=bentoml.io.Text(),
    output=bentoml.io.JSON.from_sample(
        {
            "model_id": runner.llm.model_id,
            "timeout": 3600,
            "model_name": llm_config["model_name"],
            "backend": runner.backend,
            "configuration": "",
            "supports_embeddings": runner.supports_embeddings,
            "supports_hf_agent": runner.supports_hf_agent,
        }
    ),
)
def metadata_v1(_: str) -> openllm.MetadataOutput:
    return openllm.MetadataOutput(
        timeout=llm_config["timeout"],
        model_name=llm_config["model_name"],
        backend=llm_config["env"]["backend_value"],
        model_id=runner.llm.model_id,
        configuration=llm_config.model_dump_json().decode(),
        supports_embeddings=runner.supports_embeddings,
        supports_hf_agent=runner.supports_hf_agent,
    )
