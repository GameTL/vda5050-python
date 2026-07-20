# VDA5050 adapter example (adapter_app).
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv (provisions CPython and syncs the app).
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY adapter_app/ ./

RUN uv sync

CMD ["uv", "run", "main.py"]
