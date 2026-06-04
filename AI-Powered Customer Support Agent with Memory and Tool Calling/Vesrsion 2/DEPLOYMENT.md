# 🚀 AI Customer Support Agent - Deployment Guide

**Version**: 1.0.0  
**LangChain Version**: >=1.2.0  
**Last Updated**: 2024

---

## 📋 TABLE OF CONTENTS

1. [Quick Start](#quick-start)
2. [Local Development](#local-development)
3. [Google Colab Setup](#google-colab-setup)
4. [Production Deployment](#production-deployment)
5. [Docker Deployment](#docker-deployment)
6. [API Testing](#api-testing)
7. [Troubleshooting](#troubleshooting)
8. [Monitoring & Maintenance](#monitoring--maintenance)

---

## 🚀 QUICK START

### Prerequisites
- Python 3.9+
- API Keys: GROQ_API_KEY (required), GOOGLE_API_KEY (optional)
- 2GB RAM minimum, 4GB recommended

### 5-Minute Setup (Google Colab)

```python
# 1. Open this notebook in Google Colab
# https://colab.research.google.com/

# 2. Add API keys to Colab Secrets (🔑 icon):
# - GROQ_API_KEY from https://console.groq.com

# 3. Run all cells from Phase 1 to Phase 9

# 4. Test with the provided example
```

---

## 💻 LOCAL DEVELOPMENT

### Step 1: Environment Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/customer-support-agent.git
cd customer_support_agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### Step 2: Install Dependencies (LangChain 1.2.0+)

```bash
# Create requirements.txt with exact versions
cat > requirements.txt << 'EOF'
# Core LangChain (>=1.2.0)
langchain>=1.2.0
langchain-core>=0.2.0
langchain-community>=0.2.0
langgraph>=0.1.0

# LLM Integration
langchain-groq>=0.1.0
groq>=0.7.0

# Vector Database
chromadb>=0.4.0
mem0ai>=0.1.0

# Web Framework
fastapi>=0.104.0
uvicorn[standard]>=0.24.0

# Database
sqlalchemy>=2.0
pydantic>=2.0
pydantic-settings>=2.0

# Utilities
python-dotenv>=1.0.0
requests>=2.31.0
email-validator>=2.1.0
google-genai>=0.3.0

# Testing (Optional)
pytest>=7.4.0
httpx>=0.24.0
EOF

pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Create .env file
cat > .env << 'EOF'
# LLM Configuration
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=2048

# Optional APIs
GOOGLE_API_KEY=
TAVILY_API_KEY=

# Storage Configuration
DB_PATH=data/support.db
CHROMA_RAG_DIR=data/chroma_rag
CHROMA_MEM0_DIR=data/chroma_mem0
KNOWLEDGE_BASE_DIR=knowledge_base

# RAG Configuration
RAG_CHUNK_SIZE=800
RAG_CHUNK_OVERLAP=120
RAG_TOP_K=4

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
EOF
```

### Step 4: Create Directory Structure

```bash
mkdir -p data/chroma_rag
mkdir -p data/chroma_mem0
mkdir -p knowledge_base
mkdir -p logs
```

### Step 5: Run Application

```bash
# Development mode with hot reload
python -m uvicorn customer_support_agent.main:app --reload --host 127.0.0.1 --port 8000

# Production mode
python -m uvicorn customer_support_agent.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Access the application:
- API: http://localhost:8000
- Docs: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

---

## ☁️ GOOGLE COLAB SETUP

### Step 1: Open the Notebook

1. Go to https://colab.research.google.com/
2. Upload or open the `AI_Customer_Support_Agent_Complete.ipynb` file
3. Select **T4 GPU** or **A100** from Runtime → Change runtime type

### Step 2: Configure API Keys

Click the 🔑 **Secrets** button on the left panel and add:

```
Name: GROQ_API_KEY
Value: your_api_key_from_https://console.groq.com
```

Optional secrets:
- `TAVILY_API_KEY` (for web search)
- `GOOGLE_API_KEY` (for embeddings)

### Step 3: Run Cells

Execute cells in order:
- **Phase 1**: Dependencies (3-5 minutes)
- **Phase 2**: Configuration (30 seconds)
- **Phase 3**: Integrations (1 minute)
- **Phase 4**: Services (1 minute)
- **Phase 5**: Models (30 seconds)
- **Phase 6**: Database (30 seconds)
- **Phase 7**: API Routes (30 seconds)
- **Phase 8**: App Factory (30 seconds)
- **Phase 9**: Example Usage (2-5 minutes depending on LLM)

### Step 4: Access via ngrok (Optional)

To expose the API publicly:

```python
# Install ngrok
!pip install -q pyngrok

from pyngrok import ngrok

# Get auth token from https://dashboard.ngrok.com/auth/your-authtoken
ngrok.set_auth_token("your_ngrok_token")

# Create tunnel
public_url = ngrok.connect(8000)
print(f"Public URL: {public_url}")

# Start server
import uvicorn
uvicorn.run(app, host="127.0.0.1", port=8000)
```

---

## 🌍 PRODUCTION DEPLOYMENT

### Option 1: Heroku Deployment

#### Prerequisites
- Heroku account (https://www.heroku.com)
- Heroku CLI installed
- GitHub repository

#### Deployment Steps

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set buildpack
heroku buildpacks:add heroku/python

# Create Procfile
cat > Procfile << 'EOF'
web: uvicorn customer_support_agent.main:app --host 0.0.0.0 --port $PORT
EOF

# Create runtime.txt
echo "python-3.11.7" > runtime.txt

# Set environment variables
heroku config:set GROQ_API_KEY=your_key
heroku config:set GOOGLE_API_KEY=your_key  # Optional

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Scale dynos (optional)
heroku ps:scale web=1
```

#### Verify Deployment

```bash
heroku open/api/v1/health/status
```

### Option 2: Railway Deployment

#### Prerequisites
- Railway account (https://railway.app)
- Railway CLI or GitHub connected

#### Deployment Steps

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
railway init

# Link repository
railway link

# Deploy
railway up

# View logs
railway logs
```

#### Set Environment Variables

1. Go to Railway Dashboard
2. Select project → Settings → Environment
3. Add variables:
   - `GROQ_API_KEY`
   - `PORT=8000` (automatically set)

### Option 3: Cloud Run (Google Cloud)

```bash
# Create Dockerfile (see below)
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/customer-support-agent

# Deploy to Cloud Run
gcloud run deploy customer-support-agent \
  --image gcr.io/PROJECT_ID/customer-support-agent \
  --platform managed \
  --region us-central1 \
  --set-env-vars GROQ_API_KEY=your_key \
  --memory 1Gi \
  --timeout 60
```

---

## 🐳 DOCKER DEPLOYMENT

### Step 1: Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p data/chroma_rag data/chroma_mem0 knowledge_base

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health/status || exit 1

# Run application
CMD ["uvicorn", "customer_support_agent.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2: Create Docker Compose

```yaml
version: '3.8'

services:
  # Main API
  api:
    build: .
    container_name: support-agent-api
    ports:
      - "8000:8000"
    environment:
      GROQ_API_KEY: ${GROQ_API_KEY}
      GOOGLE_API_KEY: ${GOOGLE_API_KEY:-}
      TAVILY_API_KEY: ${TAVILY_API_KEY:-}
      API_HOST: 0.0.0.0
      API_PORT: 8000
    volumes:
      - ./data:/app/data
      - ./knowledge_base:/app/knowledge_base
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health/status"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - support-agent-network

  # Optional: Standalone Chroma DB
  chroma:
    image: chromadb/chroma:latest
    container_name: support-agent-chroma
    ports:
      - "8001:8000"
    environment:
      CHROMA_DB_IMPL: duckdb+parquet
      PERSIST_DIRECTORY: /chroma/data
    volumes:
      - chroma_data:/chroma/data
    restart: unless-stopped
    networks:
      - support-agent-network

  # Optional: Nginx reverse proxy
  nginx:
    image: nginx:alpine
    container_name: support-agent-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    restart: unless-stopped
    networks:
      - support-agent-network

volumes:
  chroma_data:

networks:
  support-agent-network:
    driver: bridge
```

### Step 3: Build and Run

```bash
# Build image
docker build -t customer-support-agent:1.0.0 .

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down

# Remove volumes (careful!)
docker-compose down -v
```

### Step 4: Push to Registry

```bash
# Docker Hub
docker tag customer-support-agent:1.0.0 yourusername/customer-support-agent:1.0.0
docker push yourusername/customer-support-agent:1.0.0

# GitHub Container Registry
docker tag customer-support-agent:1.0.0 ghcr.io/yourusername/customer-support-agent:1.0.0
docker push ghcr.io/yourusername/customer-support-agent:1.0.0
```

---

## 🧪 API TESTING

### 1. Health Check

```bash
curl -s http://localhost:8000/api/v1/health/status | jq .
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "version": "1.0.0",
  "components": {
    "llm": "ok",
    "rag": "ok",
    "memory": "ok"
  }
}
```

### 2. Generate Draft

```bash
curl -X POST http://localhost:8000/api/v1/copilot/generate-draft \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "TICKET-001",
    "customer_id": "CUST-001",
    "ticket_subject": "Cannot reset password",
    "ticket_description": "I have tried to reset my password but keep getting an error",
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "customer_company": "Acme Corp"
  }'
```

### 3. Knowledge Base Search

```bash
curl -s "http://localhost:8000/api/v1/knowledge/search?q=password%20reset&top_k=3" | jq .
```

### 4. Memory Search

```bash
curl -X POST http://localhost:8000/api/v1/memory/search \
  -H "Content-Type: application/json" \
  -d '{
    "customer_email": "john@example.com",
    "query": "password reset issues",
    "limit": 5
  }'
```

### 5. Interactive API Docs

Visit http://localhost:8000/api/v1/docs for interactive Swagger documentation

---

## 🐛 TROUBLESHOOTING

### Issue 1: GROQ_API_KEY Not Found

```python
# In Colab
from google.colab import userdata
groq_key = userdata.get('GROQ_API_KEY')
print(groq_key)  # Should print your key

# In local development
import os
print(os.environ.get('GROQ_API_KEY'))  # Check if set
```

**Solution**:
- Colab: Click 🔑 Secrets button and add the key
- Local: Add to `.env` file or set with: `export GROQ_API_KEY=your_key`

### Issue 2: ChromaDB Connection Failed

```
Error: Failed to initialize ChromaDB
```

**Solutions**:
```bash
# Check directory permissions
ls -la data/chroma_rag
chmod -R 755 data/

# Reinstall ChromaDB
pip install --upgrade chromadb

# Check available disk space
df -h
```

### Issue 3: Memory System Unavailable

```python
# Check memory initialization
if copilot.memory:
    print("Memory system OK")
else:
    print("Memory system failed:", copilot._memory_error)
```

**Solutions**:
- Restart the Colab notebook
- Check ChromaDB logs: `docker logs support-agent-chroma`
- Clear chromadb cache: `rm -rf data/chroma_mem0/__pycache__`

### Issue 4: Token Limit Exceeded

```
RuntimeError: max_tokens too large
```

**Solutions**:
```python
# Reduce token limits
settings.llm_max_tokens = 1024
settings.rag_top_k = 2  # Reduce context

# Use faster model
settings.groq_model = "llama-3.1-8b-instant"
```

### Issue 5: Slow API Response

**Solutions**:
- Use 8B model instead of 70B
- Reduce `rag_top_k` from 4 to 2
- Reduce `llm_max_tokens` from 2048 to 1024
- Increase LLM temperature for faster generation

### Issue 6: Database Lock Errors

```
sqlite3.OperationalError: database is locked
```

**Solutions**:
```bash
# Check for running processes
ps aux | grep python

# Check SQLite connections
sqlite3 data/support.db ".quit"

# Restart the application
```

---

## 📊 MONITORING & MAINTENANCE

### Logging

Enable debug logging:

```python
import logging

# Set level to DEBUG
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

### Performance Monitoring

```python
# Monitor API response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/v1/health/status

# Check system resources
watch -n 1 'ps aux | grep uvicorn'
```

### Database Maintenance

```bash
# Backup database
cp data/support.db data/support.db.backup

# Backup vector store
tar -czf data/chroma_backup.tar.gz data/chroma_rag/

# Cleanup old data (optional)
sqlite3 data/support.db "DELETE FROM drafts WHERE created_at < datetime('now', '-30 days');"
```

### Monitoring Services

For production environments:

1. **Error Tracking**: Use Sentry
   ```python
   import sentry_sdk
   sentry_sdk.init("your-sentry-dsn")
   ```

2. **Application Monitoring**: Use DataDog, New Relic, or Prometheus

3. **Logging**: Use ELK Stack, Datadog, or CloudWatch

### Scaling Considerations

- **Single instance**: Handles ~100 concurrent users
- **Multi-instance**: Use load balancer (nginx, HAProxy)
- **Database**: Switch to PostgreSQL for production
- **Vector DB**: Use managed service (Pinecone, Weaviate)
- **Cache**: Add Redis for session management

---

## 🔐 SECURITY CHECKLIST

- [ ] Store API keys in secure vaults (not in code)
- [ ] Enable HTTPS/SSL in production
- [ ] Configure CORS to specific domains
- [ ] Implement API authentication (API keys, OAuth2)
- [ ] Rate limit API endpoints
- [ ] Validate all user inputs
- [ ] Regular security audits
- [ ] Keep dependencies updated: `pip list --outdated`
- [ ] Monitor for CVEs: https://cve.mitre.org/

---

## 📈 PERFORMANCE OPTIMIZATION

### 1. Reduce LLM Inference Time

```python
settings.groq_model = "llama-3.1-8b-instant"  # Faster than 70B
settings.llm_temperature = 0.1  # Lower temp = faster
settings.llm_max_tokens = 1024  # Reduce context
```

### 2. Optimize RAG

```python
settings.rag_top_k = 2  # Fewer documents
settings.rag_chunk_size = 400  # Smaller chunks
```

### 3. Cache Responses

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_customer_context(customer_email: str):
    # Cached result
    pass
```

### 4. Use Connection Pooling

```python
from sqlalchemy import create_engine

engine = create_engine(
    "sqlite:///data/support.db",
    pool_pre_ping=True,
    pool_recycle=3600,
)
```

---

## 📚 ADDITIONAL RESOURCES

- **LangChain Docs**: https://python.langchain.com/
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **Groq API**: https://console.groq.com/docs
- **ChromaDB**: https://docs.trychroma.com/
- **FastAPI**: https://fastapi.tiangolo.com/

---

**Happy Deploying! 🚀**

Last Updated: 2024
Version: 1.0.0
