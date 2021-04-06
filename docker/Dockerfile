# https://pythonspeed.com/articles/alpine-docker-python/
# https://stackoverflow.com/a/57886655/2348529
FROM python:3.9-slim as base

COPY docker/install-packages.sh .
RUN ./install-packages.sh chromium chromium-driver

RUN groupadd appgroup --system \
 && useradd appuser -g appgroup --create-home

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1



FROM base AS builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.5

RUN ./install-packages.sh build-essential \
 && pip install "poetry==$POETRY_VERSION" \
 && python -m venv /venv

COPY pyproject.toml poetry.lock ./

RUN poetry export --without-hashes -f requirements.txt \
  | /venv/bin/pip install -r /dev/stdin



FROM base as final

USER appuser
WORKDIR /home/appuser

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"
COPY app/ ./app

CMD ["--host", "0.0.0.0", "app.main:app"]
ENTRYPOINT ["uvicorn"]
