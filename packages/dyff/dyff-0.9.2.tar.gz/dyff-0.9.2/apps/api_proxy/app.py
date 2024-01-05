# Copyright UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

import os

import fastapi
import httpx
import psutil
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask

app = fastapi.FastAPI()
remote_timeout = httpx.Timeout(30, read=None)
remote = httpx.AsyncClient(base_url=os.environ["DYFF_API_URL"], timeout=remote_timeout)
api_key = os.environ["DYFF_API_KEY"]


@app.post("/terminate")
async def terminate() -> int:
    """Terminate the proxy server. Should be called as the last step of an
    audit workflow.
    """
    await remote.aclose()
    parent_pid = os.getpid()
    parent = psutil.Process(parent_pid)
    parent.terminate()
    return fastapi.status.HTTP_200_OK


@app.get(f"/health")
async def health() -> int:
    """Health check used for sidecar container lifecycle management."""
    return fastapi.status.HTTP_200_OK


async def _reverse_proxy(request: fastapi.Request) -> StreamingResponse:
    url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
    headers = request.headers.mutablecopy()
    headers["Authorization"] = f"Bearer {api_key}"
    proxy_request = remote.build_request(
        request.method, url, headers=headers.raw, content=await request.body()
    )
    proxy_response = await remote.send(proxy_request, stream=True)
    return StreamingResponse(
        proxy_response.aiter_raw(),
        status_code=proxy_response.status_code,
        headers=proxy_response.headers,
        background=BackgroundTask(proxy_response.aclose),
    )


app.add_route("/{path:path}", _reverse_proxy, ["DELETE", "GET", "PATCH", "POST", "PUT"])
