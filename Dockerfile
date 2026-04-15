# Stage1: Build dependencies
FROM python:3.11-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /build


# Copy configuration and install dependencies
COPY pyproject.toml .
RUN uv pip install --system --no-cache -r pyproject.toml --extra ml



# stage 2: Runtime environment
FROM python:3.11-slim

# Re-install modern runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    libglib2.0-0 \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


# Copy installed python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin


# Copy application source
COPY ./app ./app

ENV PYTHONPATH=/app
ENV OMP_NUM_THREADS=4


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]