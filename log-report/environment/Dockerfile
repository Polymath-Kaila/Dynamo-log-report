FROM python:3.13-slim-bookworm@sha256:05b95397cac02b060ff1251afaa78087d92d7034369afbc8eb765631cada8257

WORKDIR /app

RUN python -m pip install --no-cache-dir \
    pytest==9.1.1 \
    pytest-json-ctrf==0.5.2

COPY access.log /app/access.log
