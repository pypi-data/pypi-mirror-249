# Copyright UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
from typing import Any, Dict, List, Optional

import bentoml
import pyarrow
import transformers

from ...schema.models.tasks import classification
from .. import api
from ..outputs import classification as classification_outputs
from ..outputs import text as text_outputs


class _TransformersInterfaceBase(api.ModelInterface):
    @abc.abstractproperty
    def input_descriptor(self) -> str:
        raise NotImplementedError()

    @abc.abstractproperty
    def task_name(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_pipeline(self, local_path: str) -> transformers.Pipeline:
        raise NotImplementedError()

    @property
    def inference_kwargs(self) -> Optional[Dict[str, Any]]:
        return None

    @property
    def output_descriptor(self) -> str:
        return "bentoml.io.JSON()"

    @abc.abstractproperty
    def required_packages(self) -> List[str]:
        raise NotImplementedError()

    def prepare_bento_model(
        self, local_path: str, model_tag: str
    ) -> api.BentoBuildSpec:
        pipeline = self.create_pipeline(local_path)
        bentoml.transformers.save_model(name=model_tag, pipeline=pipeline)
        python_packages = list(sorted(self.required_packages))
        bentofile = {"labels": {}, "python": {"packages": python_packages}}
        return api.BentoBuildSpec(
            input_descriptor=self.input_descriptor,
            output_descriptor=self.output_descriptor,
            bentofile=bentofile,
            inference_kwargs=self.inference_kwargs,
        )


class ImageClassification(_TransformersInterfaceBase):
    def __init__(self, task: classification.Classification):
        self._task = task

    @property
    def inference_task(self) -> classification.Classification:
        return self._task

    @property
    def output_spec(self) -> classification_outputs.Scores:
        return classification_outputs.Scores(self._task)

    def _rpc_encode_input(self, item: Dict) -> api.HTTPPayload:
        headers = {"content-type": item["image"]["format"]}
        data = item["image"]["bytes"]
        return api.HTTPPayload(headers=headers, data=data)

    def _rpc_decode_output(self, item: Any) -> Dict[str, Any]:
        keys = ["label", "score"]
        result_dict = {k: [] for k in keys}
        for d in item:
            for k in keys:
                result_dict[k].append(d[k])
        return result_dict

    @property
    def inference_kwargs(self) -> Optional[Dict[str, Any]]:
        return {"top_k": self.inference_task.numLabels}

    @property
    def input_descriptor(self) -> str:
        return "bentoml.io.Image()"

    @property
    def required_packages(self) -> List[str]:
        # return super().required_packages + ["pillow"]
        return ["transformers[torch,torch-vision,vision]"]

    @property
    def task_name(self):
        return "image-classification"

    def create_pipeline(self, local_path: str) -> transformers.Pipeline:
        feature_extractor = transformers.AutoFeatureExtractor.from_pretrained(
            local_path
        )
        model = transformers.AutoModelForImageClassification.from_pretrained(local_path)
        return transformers.pipelines.pipeline(
            self.task_name, model=model, feature_extractor=feature_extractor
        )


class TokenClassification(_TransformersInterfaceBase):
    class OutputSpecification(text_outputs.TaggedSpans):
        def _fields(self):
            return [
                pyarrow.field(
                    "spans",
                    pyarrow.list_(
                        pyarrow.struct(
                            [
                                pyarrow.field("start", pyarrow.int64()),
                                pyarrow.field("end", pyarrow.int64()),
                                pyarrow.field("tag", pyarrow.string()),
                                pyarrow.field("score", pyarrow.float32()),
                                pyarrow.field("word", pyarrow.string()),
                            ]
                        )
                    ),
                )
            ]

        # Apparently we can't verify this because some models insert whitespace
        # in between tokens in their 'word' output.
        # def verify_output(self, item):
        #   super().verify_output(item)
        #   for span in item["spans"]:
        #     if len(span["word"]) != (span["end"] - span["start"]):
        #       raise FieldFormatError(
        #         f"word {span['word']} : length != end - start ({span['start']}, {span['end']})")

    def __init__(self, task: classification.Classification):
        self._task = task

    @property
    def inference_task(self) -> classification.Classification:
        return self._task

    @property
    def output_spec(self) -> TokenClassification.OutputSpecification:
        return TokenClassification.OutputSpecification(self._task)

    def _rpc_encode_input(self, item: Dict) -> api.HTTPPayload:
        headers = {"content-type": "text/plain"}
        data = item["text"]
        return api.HTTPPayload(headers=headers, data=data)

    def _rpc_decode_output(self, item: Any) -> Dict[str, Any]:
        def remove_leading_double_hash(word):
            if word.startswith("##"):
                return word[2:]
            else:
                return word

        return {
            "spans": [
                {
                    "start": span["start"],
                    "end": span["end"],
                    "tag": span["entity_group"],
                    "score": span["score"],
                    # There are tokens like "##foo" if the model says that an entity
                    # starts in the middle of a word
                    "word": remove_leading_double_hash(span["word"]),
                }
                for span in item
            ]
        }

    @property
    def inference_kwargs(self) -> Optional[Dict[str, Any]]:
        # This is the default behavior for HF Web-hosted models
        # See: https://huggingface.co/docs/api-inference/detailed_parameters#token-classification-task
        return {"aggregation_strategy": "simple"}

    @property
    def input_descriptor(self) -> str:
        return "bentoml.io.Text()"

    @property
    def required_packages(self) -> List[str]:
        # return super().required_packages + ["transformers[sentencepiece]"]
        return ["transformers[torch,sentencepiece,tokenizers]"]

    @property
    def task_name(self):
        return "ner"

    def create_pipeline(self, local_path: str) -> transformers.Pipeline:
        tokenizer = transformers.AutoTokenizer.from_pretrained(local_path)
        model = transformers.AutoModelForTokenClassification.from_pretrained(local_path)
        return transformers.pipelines.pipeline(
            self.task_name, model=model, tokenizer=tokenizer
        )
