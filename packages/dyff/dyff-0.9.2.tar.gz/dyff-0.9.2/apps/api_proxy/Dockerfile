ARG CONTAINER_PROXY
FROM ${CONTAINER_PROXY}python:3.9-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE="1" \
    PYTHONUNBUFFERED="1"

# hadolint ignore=DL3013
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel

WORKDIR /apps/proxy/

COPY requirements.txt ./

RUN python3 -m pip install --no-cache-dir -r ./requirements.txt

COPY . ./

ENTRYPOINT ["python3", "app.py"]
