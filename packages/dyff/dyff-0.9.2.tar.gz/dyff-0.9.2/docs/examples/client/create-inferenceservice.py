# Copyright UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

from dyff.client import Client
from dyff.schema.platform import (
    Accelerator,
    AcceleratorGPU,
    DataSchema,
    DyffDataSchema,
    InferenceInterface,
    InferenceServiceRunner,
    InferenceServiceRunnerKind,
    ModelResources,
    SchemaAdapter,
)
from dyff.schema.requests import InferenceServiceCreateRequest

API_KEY: str = ...
ACCOUNT: str = ...

dyffapi = Client(api_key=API_KEY)

service_request = InferenceServiceCreateRequest(
    account=ACCOUNT,
    # The vLLM runner currently downloads the model weights at runtime, so
    # there is no data to access
    model=None,
    name="databricks/dolly-v2-3b",
    runner=InferenceServiceRunner(
        kind=InferenceServiceRunnerKind.VLLM,
        # T4 GPUs don't support bfloat format, so force standard float format
        args=["--dtype", "float16"],
        accelerator=Accelerator(
            kind="GPU",
            gpu=AcceleratorGPU(
                hardwareTypes=["nvidia.com/gpu-t4"],
                memory="10Gi",
            ),
        ),
        resources=ModelResources(
            storage="10Gi",
            memory="16Gi",
        ),
    ),
    interface=InferenceInterface(
        # This is the inference endpoint for the vLLM runner
        endpoint="generate",
        # The output records should look like: {"text": "To be, or not to be"}
        outputSchema=DataSchema.make_output_schema(
            DyffDataSchema(
                components=["text.Text"],
                version="v0",
            ),
        ),
        # How to convert the input dataset into the format the runner expects
        inputPipeline=[
            # {"text": "The question"} -> {"prompt": "The question"}
            SchemaAdapter(
                kind="TransformJSON",
                configuration={"prompt": "$.text"},
            ),
        ],
        # How to convert the runner output to match outputSchema
        outputPipeline=[
            # {"text": ["The answer"]} -> {"text": "The answer"}
            SchemaAdapter(
                kind="ExplodeCollections",
                configuration={"collections": ["text"]},
            ),
        ],
    ),
)

service = dyffapi.inferenceservices.create(service_request)
print(f"created inferenceservice:\n{service}")
