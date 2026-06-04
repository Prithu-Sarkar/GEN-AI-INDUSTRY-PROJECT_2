# 🤖 AI-Powered Customer Support Agent with Memory & Tool Calling

A production-ready AI customer support system built with **LangChain 1.2.0+**, **LangGraph**, **Groq API**, and **ChromaDB**.

![Status](https://img.shields.io/badge/status-production--ready-brightgreen)
![LangChain](https://img.shields.io/badge/LangChain-1.2.0%2B-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Features

| Feature | Description | Status |
|---------|-------------|--------|
| **🤖 AI Agent** | LangGraph-based agent with tool calling | ✅ |
| **💾 Memory System** | Persistent customer memory (Mem0 + ChromaDB) | ✅ |
| **📚 RAG** | Knowledge base semantic search | ✅ |
| **🛠️ Tools** | Dynamic tool execution for customer lookups | ✅ |
| **🔌 API** | FastAPI with dependency injection | ✅ |
| **💾 Database** | SQLAlchemy + SQLite | ✅ |
| **🚀 Deployable** | Docker, Heroku, Railway, Cloud Run | ✅ |
| **📊 Monitoring** | Health checks and performance metrics | ✅ |

---

## 🚀 Quick Start

### Google Colab (Recommended for Beginners)

```python
# 1. Open notebook in Google Colab
# https://colab.research.google.com/

# 2. Upload: AI_Customer_Support_Agent_Complete.ipynb

# 3. Add API keys to Colab Secrets (🔑 icon):
GROQ_API_KEY = your_key_from_https://console.groq.com

# 4. Run all cells from Phase 1 to Phase 9
# Done! ✅
```

### Local Development

```bash
# Clone repo
git clone https://github.com/yourusername/customer-support-agent.git
cd customer_support_agent

# Setup environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure .env
cp .env.example .env
# Edit .env with your GROQ_API_KEY

# Create directories
mkdir -p data/chroma_rag data/chroma_mem0 knowledge_base

# Run server
python -m uvicorn customer_support_agent.main:app --reload

# Access
# API: http://localhost:8000
# Docs: http://localhost:8000/api/v1/docs
```

---

## 📋 Project Structure

```
customer_support_agent/
├── 📄 AI_Customer_Support_Agent_Complete.ipynb
│   ├── PHASE 1️⃣: Environment Setup
│   ├── PHASE 2️⃣: Configuration
│   ├── PHASE 3️⃣: Integrations (Tools, Memory, RAG)
│   ├── PHASE 4️⃣: Core Services
│   ├── PHASE 5️⃣: Data Models
│   ├── PHASE 6️⃣: Database
│   ├── PHASE 7️⃣: API Routes
│   ├── PHASE 8️⃣: App Factory
│   ├── PHASE 9️⃣: Testing & Examples
│   └── PHASE 🔟: Deployment
│
├── 📁 data/
│   ├── support.db                  # SQLite database
│   ├── chroma_rag/                 # RAG vector store
│   └── chroma_mem0/                # Memory vector store
│
├── 📁 knowledge_base/
│   ├── password_reset.md
│   ├── error_codes.md
│   └── ...
│
├── 📄 requirements.txt
├── 📄 .env.example
├── 📄 DEPLOYMENT.md                # Step-by-step deployment
├── 📄 README.md                    # This file
├── 📄 Dockerfile
├── 📄 docker-compose.yml
└── 📄 nginx.conf
```

---

## 🔑 API Keys Required

| Service | Purpose | Cost | Get It |
|---------|---------|------|--------|
| **GROQ_API_KEY** | LLM (Llama 3.1) | Free | [console.groq.com](https://console.groq.com) |
| GOOGLE_API_KEY | Embeddings | Free | [ai.google.dev](https://ai.google.dev) |
| TAVILY_API_KEY | Web search | Free | [tavily.com](https://tavily.com) |

---

## 📦 Dependencies

### Core Versions (Pinned)

```
✅ LangChain: >=1.2.0 (Latest)
✅ LangGraph: >=0.1.0 (Latest)
✅ Groq: >=0.7.0 (Latest)
✅ FastAPI: >=0.104.0
✅ Pydantic: >=2.0
✅ ChromaDB: >=0.4.0
```

**Note**: This notebook requires **LangChain 1.2.0 or higher**. Earlier versions (like 0.2.x) will NOT work due to API changes.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│             Client Application                   │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│        FastAPI Web Framework                    │
│  (8 endpoints: copilot, knowledge, memory)     │
└────────────────┬────────────────────────────────┘
                 │
    ┌────────────┼────────────┬──────────────┐
    ▼            ▼            ▼              ▼
┌────────┐  ┌──────┐  ┌──────────┐  ┌──────────┐
│ Tools  │  │ RAG  │  │ Memory   │  │ Database │
│        │  │      │  │          │  │          │
│ - Plan │  │ KB   │  │ Mem0 +   │  │SQLAlchemy│
│ - Bill │  │      │  │ChromaDB  │  │SQLite    │
│ - Tkt  │  │      │  │          │  │          │
│ - Acct │  │      │  │          │  │          │
└────────┘  └──────┘  └──────────┘  └──────────┘
    │            │            │              │
    └────────────┴────────────┴──────────────┘
                 │
                 ▼
    ┌────────────────────────────┐
    │   LangChain 1.2.0+         │
    │   ChatGroq + LangGraph     │
    │   Agent with Checkpoints   │
    └────────────────────────────┘
                 │
                 ▼
    ┌────────────────────────────┐
    │   Groq API (Llama 3.1)     │
    │   6000 TPM Free Tier       │
    └────────────────────────────┘
```

---

## 💻 API Endpoints

### Copilot Service

```
POST   /api/v1/copilot/generate-draft    Generate AI response
GET    /api/v1/copilot/tickets/{id}      Get ticket details
```

### Knowledge Base

```
GET    /api/v1/knowledge/search          Search docs
POST   /api/v1/knowledge/load            Load from folder
```

### Memory

```
POST   /api/v1/memory/search             Search memories
GET    /api/v1/memory/customer/{email}   List customer memories
```

### Health

```
GET    /api/v1/health/status             Health check
GET    /api/v1/health/version            Version info
```

---

## 🧪 Example Usage

### 1. Generate Support Draft

```bash
curl -X POST http://localhost:8000/api/v1/copilot/generate-draft \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "TICKET-001",
    "customer_id": "CUST-001",
    "ticket_subject": "Cannot export reports",
    "ticket_description": "When I click export, I get error 502",
    "customer_name": "Jane Doe",
    "customer_email": "jane@company.com",
    "customer_company": "TechCorp Inc"
  }'
```

### 2. Search Knowledge Base

```bash
curl "http://localhost:8000/api/v1/knowledge/search?q=password%20reset&top_k=3"
```

### 3. Search Customer Memory

```bash
curl -X POST http://localhost:8000/api/v1/memory/search \
  -H "Content-Type: application/json" \
  -d '{
    "customer_email": "jane@company.com",
    "query": "export issues",
    "limit": 5
  }'
```

---

## 🚀 Deployment Options

### Colab (Free)
- No setup required
- GPU available
- Perfect for learning
- See Phase 1-2 in notebook

### Local (Development)
- Full control
- Easy debugging
- See DEPLOYMENT.md: "Local Development"

### Heroku (Easy)
- One-click deploy
- Free tier available
- See DEPLOYMENT.md: "Heroku Deployment"

### Docker (Scalable)
- Container-based
- Production-ready
- See DEPLOYMENT.md: "Docker Deployment"

### Cloud Run / Railway (Modern)
- Serverless
- Auto-scaling
- See DEPLOYMENT.md: "Production Deployment"

---

## 🔧 Configuration

### Key Environment Variables

```env
# LLM
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.1-8b-instant
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=2048

# Storage
DB_PATH=data/support.db
CHROMA_RAG_DIR=data/chroma_rag
CHROMA_MEM0_DIR=data/chroma_mem0

# RAG
RAG_CHUNK_SIZE=800
RAG_CHUNK_OVERLAP=120
RAG_TOP_K=4
MEM0_TOP_K=5

# API
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 📊 Performance Tips

### Speed Up Inference

```python
# Use 8B model instead of 70B
settings.groq_model = "llama-3.1-8b-instant"

# Reduce context
settings.rag_top_k = 2
settings.llm_max_tokens = 1024
```

### Reduce Token Usage

```python
# Lower temperature for faster response
settings.llm_temperature = 0.1

# Smaller chunks
settings.rag_chunk_size = 400
```

---

## 🛠️ Troubleshooting

### GROQ_API_KEY Not Found

**Colab**: Click 🔑 Secrets → Add `GROQ_API_KEY`  
**Local**: Add to `.env` or run: `export GROQ_API_KEY=your_key`

### ChromaDB Issues

```bash
# Check directory
ls -la data/chroma_rag

# Fix permissions
chmod -R 755 data/

# Reinstall
pip install --upgrade chromadb
```

### Token Limit Exceeded

**Solution**: Use 8B model and reduce token limits
```python
settings.llm_max_tokens = 1024
```

### Memory System Unavailable

**Solution**: Check ChromaDB initialization
```python
print(copilot._memory_error)  # Shows error if any
```

See DEPLOYMENT.md for more troubleshooting!

---

## 📚 Learning Resources

| Resource | Link |
|----------|------|
| LangChain 1.2.0 Docs | https://python.langchain.com/ |
| LangGraph Docs | https://langchain-ai.github.io/langgraph/ |
| Groq Console | https://console.groq.com/docs |
| ChromaDB Docs | https://docs.trychroma.com/ |
| FastAPI Docs | https://fastapi.tiangolo.com/ |

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Open a Pull Request

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🙋 Support

### Issues & Questions

- **Documentation**: See DEPLOYMENT.md
- **API Docs**: Visit `/api/v1/docs` in running application
- **GitHub Issues**: Open an issue in the repository

### Quick Links

- 🐛 **Bug Reports**: Include logs and error messages
- 💡 **Feature Requests**: Describe use case
- 📖 **Documentation**: Help improve docs
- 🧪 **Testing**: Test on different environments

---

## 🎓 What You'll Learn

After completing this project, you'll understand:

- ✅ Building LangChain 1.2.0+ applications
- ✅ Implementing agents with LangGraph
- ✅ Designing memory and RAG systems
- ✅ Creating production APIs with FastAPI
- ✅ Deploying AI applications
- ✅ Managing tool calling and function execution
- ✅ Handling context windows efficiently

---

## 📈 Roadmap

- [ ] Add authentication (API keys, OAuth2)
- [ ] Integrate with ticketing systems (Zendesk, Intercom)
- [ ] Advanced RAG with re-ranking
- [ ] Fine-tuned model support
- [ ] Multi-language support
- [ ] Advanced monitoring dashboard
- [ ] GraphQL API option

---

## 🚀 Get Started Now!

1. **Google Colab** (Recommended): Open the notebook and run!
2. **Local**: Clone the repo and follow Local Development section
3. **Production**: Follow the deployment guide

**Questions?** Check DEPLOYMENT.md or the notebook documentation.

---

**Happy Building! 🎉**

Made with ❤️ using LangChain 1.2.0+ | Last Updated: 2024
