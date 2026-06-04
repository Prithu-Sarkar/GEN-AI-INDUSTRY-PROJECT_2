# =====================================================
# AI Customer Support Agent - Dockerfile
# Production-ready Docker image
# =====================================================

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/chroma_rag \
    data/chroma_mem0 \
    knowledge_base \
    logs

# Set permissions
RUN chmod -R 755 data/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health/status || exit 1

# Run application
CMD ["uvicorn", "customer_support_agent.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
