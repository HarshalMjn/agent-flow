FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ \
    build-essential \
    python3-dev \
    libmariadb-dev-compat \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

ENV PATH="/code/.venv/bin:$PATH"

ENV UV_COMPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

# Sync dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project

ENV PYTHONPATH=/code

COPY ./pyproject.toml /code/
# Note uv.lock is not copied yet, but uv sync will create it or use it if present.
# We'll touch uv.lock if it doesn't exist to satisfy the bind mount in future builds.

COPY ./alembic.ini /code/

COPY ./app /code/app

COPY ./scripts /code/scripts

COPY ./alembic /code/alembic

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

EXPOSE 8000

CMD ["fastapi", "run", "--workers", "2", "app/main.py"]
