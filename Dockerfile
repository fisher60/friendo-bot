ARG python_version=3.14-slim

FROM python:$python_version AS builder
COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /bin/

ENV UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy

# Install project dependencies with build tools available
WORKDIR /build

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project

# -------------------------------------------------------------------------------

FROM python:$python_version

ARG git_sha="development"
ENV GIT_SHA=$git_sha

# Define version build argument
ARG version="development"
ENV VERSION=$version

# Install dependencies from build cache
# .venv not put in /app so that it doesn't conflict with the dev
# volume we use to avoid rebuilding image every code change locally
COPY --from=builder /build /build
ENV PATH="/build/.venv/bin:$PATH"

# Copy the source code in last to optimize rebuilding the image
WORKDIR /app
COPY . .

ENTRYPOINT ["python", "-m"]
CMD ["bot"]
