FROM python:3.12 AS builder
LABEL authors="nicolasoliveto"

WORKDIR /apiapp

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.12
LABEL authors="nicolasoliveto"

WORKDIR /apiapp

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY /app ./app

COPY coin_mining.py .

RUN apt-get update && \
    apt-get install -y cron gcc libpq-dev --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /apiapp/logs/

RUN mkdir -p /apiapp/data

VOLUME /apiapp/data

ENTRYPOINT ["/bin/bash", "-i"]
