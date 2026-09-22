# -----------------------------------
# Stage 1: Build the React Frontend
# -----------------------------------
FROM node:18-alpine AS frontend-builder
WORKDIR /frontend

# Install dependencies and build
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# -----------------------------------
# Stage 2: Build the FastAPI Backend
# -----------------------------------
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    WORKSPACE_TTL_SECONDS=3600 \
    WORKSPACE_CLEANUP_INTERVAL_SECONDS=60

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install CPU-only PyTorch wheel to minimize image size and build latency
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-cache the cross-encoder reranker model so cold starts don't block
RUN python -c "from sentence_transformers import CrossEncoder; CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')"

# Copy backend source code
COPY app/ app/
COPY src/ src/

# Copy built frontend from Stage 1
COPY --from=frontend-builder /frontend/dist /app/frontend/dist

# Ephemeral user documents root
RUN mkdir -p data/user_documents

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
