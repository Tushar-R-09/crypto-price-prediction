# ---------- Builder Stage ----------
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Build and install TA-Lib
WORKDIR /build
ENV TALIB_DIR=/usr/local

RUN wget https://github.com/ta-lib/ta-lib/releases/download/v0.6.4/ta-lib-0.6.4-src.tar.gz && \
    tar -xzf ta-lib-0.6.4-src.tar.gz && \
    cd ta-lib-0.6.4 && \
    ./configure --prefix=$TALIB_DIR && \
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

# Copy services and dependencies
COPY services /app/services
COPY pyproject.toml uv.lock /app/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies without source code
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy full source code
COPY . /app

# Final install with source
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Activate virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Reset entrypoint
ENTRYPOINT []

# Default command to run candles service
CMD ["uv", "run", "/app/services/candles/src/candles/main.py"]

# For debugging (uncomment if needed)
# CMD ["/bin/bash", "-c", "sleep 9999999"]
