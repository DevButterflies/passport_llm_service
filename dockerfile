# ----------------------------
# 🏗 Stage 1: Build environment
# ----------------------------
FROM python:3.11-slim AS builder
WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --user --no-cache-dir -r requirements.txt

# ----------------------------
# 🚀 Stage 2: Runtime environment
# ----------------------------
FROM python:3.11-slim
# We set WORKDIR to root so 'app' is a visible module
WORKDIR /

RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libsm6 libxext6 libxrender1 libgomp1 libgl1 ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
# Ensure current directory is in Python path
ENV PYTHONPATH=/

# Copy the app folder into /app
COPY ./app /app

# IMPORTANT: Ensure logs directory exists
RUN mkdir -p /logs

EXPOSE 8001

# Run using the module flag from the root
CMD ["python", "-m", "app.main"]