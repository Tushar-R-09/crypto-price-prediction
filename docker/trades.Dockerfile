# ---------- Builder Stage ----------
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Build and install TA-Lib to a temporary location
WORKDIR /build
RUN wget https://github.com/ta-lib/ta-lib/releases/download/v0.6.4/ta-lib-0.6.4-src.tar.gz && \
    tar -xzf ta-lib-0.6.4-src.tar.gz && \
    cd ta-lib-0.6.4 && \
    ./configure --prefix=/usr/local && \
    make -j$(nproc) && \
    make install

# Prepare app dependencies
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY services /app/services
COPY pyproject.toml uv.lock /app/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# ---------- Final Slim Stage ----------
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Copy compiled TA-Lib from builder
COPY --from=builder /usr/local/lib/libta_lib.* /usr/local/lib/
COPY --from=builder /usr/local/include/ta-lib /usr/local/include/
RUN ldconfig

# Set up app directory
WORKDIR /app

# Copy only required files
COPY services /app/services
COPY pyproject.toml uv.lock /app/

# Install dependencies
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy the rest of the source code
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Update PATH for virtualenv
ENV PATH="/app/.venv/bin:$PATH"

# Reset entrypoint
ENTRYPOINT []

# Default command
CMD ["uv", "run", "/app/services/trades/src/trades/main.py"]

# Debug option (commented)
# CMD ["/bin/bash", "-c", "sleep 9999999"]
