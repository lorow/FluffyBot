FROM python:3.9-slim as base

ENV PATH /root/.local/bin:$PATH

WORKDIR /app
COPY . .

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

RUN apt install git && \
    python3 -m pip install poetry && \
    poetry install && \
    poetry run python -m pip install git+git://github.com/aio-libs/aioredis-py.git@master

CMD ["poetry", "run", "python", "fluffy.py"]