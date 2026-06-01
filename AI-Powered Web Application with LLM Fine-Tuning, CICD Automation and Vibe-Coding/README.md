<div align="center">

<img src="https://img.shields.io/badge/Azure%20AI%20Foundry-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white" />
<img src="https://img.shields.io/badge/AWS%20CodePipeline-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" />
<img src="https://img.shields.io/badge/React%2019-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
<img src="https://img.shields.io/badge/LangChain%201.2.0-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" />
<img src="https://img.shields.io/badge/Groq%20LLaMA-F55036?style=for-the-badge&logo=meta&logoColor=white" />
<img src="https://img.shields.io/badge/Vite%207-646CFF?style=for-the-badge&logo=vite&logoColor=white" />

<br /><br />

# 🤖 Fine-Tune LLM · Azure AI Foundry + AWS CI/CD

### End-to-End LLM Fine-Tuning Pipeline with Streaming Chat UI and Automated Cloud Deployment

<p align="center">
  <b>Synthetic Data Generation → GPT-4o Fine-Tuning → React Chat Interface → AWS CodePipeline → S3 Static Hosting</b>
</p>

<br />

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Node](https://img.shields.io/badge/Node.js-18%2B-339933?style=flat-square&logo=nodedotjs&logoColor=white)](https://nodejs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![LangChain](https://img.shields.io/badge/LangChain-1.2.0-1C3C3C?style=flat-square)](https://python.langchain.com)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Phase 1 · Data Generation](#-phase-1--synthetic-data-generation)
- [Phase 2 · Azure AI Foundry Fine-Tuning](#-phase-2--azure-ai-foundry-fine-tuning)
- [Phase 3 · React Chat Application](#-phase-3--react-chat-application)
- [Phase 4 · AWS CI/CD Deployment](#-phase-4--aws-cicd-deployment)
- [Environment Variables](#-environment-variables)
- [API Reference](#-api-reference)
- [Dataset Format](#-dataset-format)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔭 Overview

This repository delivers a **production-ready, end-to-end LLM engineering pipeline** that spans every layer of the modern AI stack — from raw data synthesis to a live, auto-deployed chat product.

| What it does | How |
|---|---|
| Generates 400–600 high-quality fine-tuning examples | Groq `llama-3.1-8b-instant` via **LangChain 1.2.0** |
| Fine-tunes GPT-4o on a custom Customer-Support persona | **Azure AI Foundry** managed fine-tuning |
| Serves the model through a sleek streaming chat UI | **React 19 + Vite 7**, direct Azure OpenAI SSE |
| Deploys automatically on every `git push` | **AWS CodePipeline → CodeBuild → S3** static hosting |

> **Use case:** A customer-support bot trained to behave as a professional, empathetic agent — capable of handling order tracking, returns, account issues, escalations, and AI project mentoring — deployed at zero infrastructure cost.

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DEVELOPMENT PHASE                            │
│                                                                     │
│  ┌─────────────┐    LangChain 1.2.0     ┌──────────────────────┐   │
│  │  Topic      │ ──── LCEL Chain ────▶  │  Groq LLaMA-3.1      │   │
│  │  Taxonomy   │                        │  (llama-3.1-8b-       │   │
│  │  (7 cats)   │ ◀── JSON response ──   │   instant)            │   │
│  └─────────────┘                        └──────────────────────┘   │
│         │                                                           │
│         ▼                                                           │
│  ┌─────────────────────────────────────┐                           │
│  │   train.jsonl  (400 examples)       │                           │
│  │   validation.jsonl (50 examples)    │  ← JSONL Chat Format      │
│  └─────────────────────────────────────┘                           │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼ Upload
┌─────────────────────────────────────────────────────────────────────┐
│                     AZURE AI FOUNDRY                                │
│                                                                     │
│   GPT-4o Base  ──── Fine-Tuning Job ────▶  GPT-4o Fine-Tuned      │
│   (gpt-4o-2024-08-06)      ↑                   │                   │
│                      train.jsonl                ▼                   │
│                      validation.jsonl    Deployment Endpoint        │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼ API Key + Endpoint
┌─────────────────────────────────────────────────────────────────────┐
│                     REACT CHAT APPLICATION                          │
│                                                                     │
│  ┌──────────┐  ┌───────────┐  ┌────────────┐  ┌────────────────┐  │
│  │ Sidebar  │  │  TopBar   │  │  Messages  │  │  ConfigModal   │  │
│  │(Sessions)│  │(Status)   │  │ (Streaming)│  │(Azure Creds)   │  │
│  └──────────┘  └───────────┘  └────────────┘  └────────────────┘  │
│                                                                     │
│       Direct Azure OpenAI SSE Streaming (no backend needed)        │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼ git push → webhook
┌─────────────────────────────────────────────────────────────────────┐
│                      AWS CI/CD PIPELINE                             │
│                                                                     │
│  GitHub ──▶ CodePipeline ──▶ CodeBuild ──▶ S3 Static Website      │
│  (source)    (orchestrate)   (npm build)   (public URL)            │
│                                                                     │
│         buildspec.yml  ·  Node 18  ·  npm ci  ·  vite build        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
project-root/
│
├── 📁 DATA JSONL FILES/          # Fine-tuning datasets
│   ├── train.jsonl               # 400 training examples (chat format)
│   ├── validation.jsonl          # 50 validation examples
│   ├── token_distribution.png   # Token stats visualization
│   └── category_distribution.png
│
├── 📁 src/                       # React application source
│   ├── App.jsx                   # Root component + streaming logic
│   ├── App.css                   # Base styles
│   ├── index.css                 # Full design system (dark theme)
│   ├── main.jsx                  # React DOM entry point
│   └── 📁 components/
│       ├── ChatInput.jsx         # Auto-resize textarea + send button
│       ├── ChatMessages.jsx      # Message bubbles + typing indicator
│       ├── ConfigModal.jsx       # Azure credentials modal
│       ├── Sidebar.jsx           # Session history sidebar
│       └── TopBar.jsx            # Status bar + actions
│
├── 📁 server/                    # Optional Express backend (SSE proxy)
│   ├── index.js                  # Azure OpenAI streaming proxy
│   └── package.json
│
├── 📁 public/
│   └── vite.svg
│
├── index.html                    # App shell
├── vite.config.js                # Vite configuration
├── package.json                  # Frontend dependencies
├── buildspec.yml                 # AWS CodeBuild specification
├── .gitignore
└── README.md                     # This file
```

---

## 🛠 Tech Stack

### Data & AI Layer
| Technology | Version | Purpose |
|---|---|---|
| **LangChain Core** | 1.2.0 | LCEL chains, prompt templates, output parsers |
| **LangChain Community** | 1.2.0 | Callbacks, community integrations |
| **LangChain Groq** | 0.3.2 | Groq LLM integration |
| **Groq SDK** | 0.28.0 | Direct Groq API access |
| **Azure AI Foundry** | — | GPT-4o fine-tuning & deployment |
| **tiktoken** | 0.9.0 | Token counting & validation |
| **datasets** | 3.6.0 | Dataset management |

### Frontend Layer
| Technology | Version | Purpose |
|---|---|---|
| **React** | 19.2.0 | UI framework |
| **Vite** | 7.3.1 | Build tool & dev server |
| **Azure OpenAI SDK** | — | Direct SSE streaming |
| **Inter Font** | — | Typography (Google Fonts) |

### Infrastructure Layer
| Technology | Purpose |
|---|---|
| **AWS CodePipeline** | CI/CD orchestration |
| **AWS CodeBuild** | Build environment (Node 18) |
| **Amazon S3** | Static website hosting |
| **Amazon CloudFront** | CDN + HTTPS (optional) |
| **GitHub Webhooks** | Auto-trigger on push |

---

## ✅ Prerequisites

### Python Environment
```bash
Python >= 3.10
pip (latest)
```

### Node.js Environment
```bash
Node.js >= 18.0.0
npm >= 9.0.0
```

### Cloud Accounts
- **Azure** subscription with [Azure OpenAI access approved](https://aka.ms/oai/access)
- **AWS** account with IAM permissions for: CodePipeline, CodeBuild, S3
- **Groq** API key — free tier at [console.groq.com](https://console.groq.com)

---

## ⚡ Quick Start

### 1 · Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/Finetune-LLM-Azure-Foundry-and-CICD-using-AWS.git
cd Finetune-LLM-Azure-Foundry-and-CICD-using-AWS
```

### 2 · Set up Python environment
```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install langchain==1.2.0 \
            langchain-core==1.2.0 \
            langchain-community==1.2.0 \
            langchain-groq==0.3.2 \
            groq==0.28.0 \
            tiktoken==0.9.0 \
            datasets==3.6.0 \
            jsonlines==4.0.0 \
            pandas matplotlib seaborn tqdm
```

### 3 · Configure secrets
```bash
export GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxx"

# After Azure fine-tuning is complete:
export AZURE_ENDPOINT="https://your-resource.cognitiveservices.azure.com/"
export AZURE_API_KEY="your-azure-openai-key"
export AZURE_DEPLOYMENT="gpt-4o-2024-08-06-project-demo"
```

### 4 · Run the notebook
Open `Finetune_LLM_Azure_Foundry_CICD_AWS.ipynb` and run all cells in order.

### 5 · Start the React app
```bash
npm install
npm run dev                        # http://localhost:5173
```

---

## 📊 Phase 1 · Synthetic Data Generation

The pipeline uses a **LangChain 1.2.0 LCEL chain** to generate diverse, high-quality fine-tuning data:

```python
# LangChain 1.2.0 — LCEL pipe syntax
generation_chain = (
    ChatPromptTemplate.from_messages([...])
    | ChatGroq(model="llama-3.1-8b-instant")
    | StrOutputParser()
)
```

### Dataset Composition

| Category | Topics Covered | Complexity Levels |
|---|---|---|
| `order_tracking` | Tracking, delivery status, shipping times | Beginner → Advanced |
| `returns_refunds` | Return policy, refund timelines, exchanges | Beginner → Advanced |
| `account_issues` | Password reset, email change, billing | Beginner → Advanced |
| `product_questions` | Warranty, specs, compatibility | Beginner → Advanced |
| `technical_support` | App crashes, checkout errors, promo codes | Intermediate → Advanced |
| `escalation` | Manager requests, repeated issues | Advanced |
| `ai_project_mentor` | ML projects, MLOps, architecture | Intermediate → Advanced |

### Output Format (Azure OpenAI JSONL)

```jsonl
{
  "messages": [
    {"role": "system",    "content": "You are a professional customer support assistant..."},
    {"role": "user",      "content": "My order hasn't arrived after 5 days."},
    {"role": "assistant", "content": "I'm sorry to hear that. Let me look into this for you..."},
    {"role": "user",      "content": "My order number is ORD-2024-98765."},
    {"role": "assistant", "content": "Thank you. I can see your order is currently in transit..."}
  ]
}
```

### Dataset Statistics

| Split | Examples | Avg Tokens | Avg Turns |
|---|---|---|---|
| Training | 400 | ~180 | 5 |
| Validation | 50 | ~120 | 3 |

> **Rate limiting note:** The default configuration sleeps 1.5 seconds between API calls to stay within Groq's free-tier limits (`~6,000 TPM` for `llama-3.1-8b-instant`). Adjust `SLEEP_BETWEEN` in the notebook if needed.

---

## 🔷 Phase 2 · Azure AI Foundry Fine-Tuning

### Step-by-Step

**1. Upload data**
- Navigate to [ai.azure.com](https://ai.azure.com) → **Fine-tuning** → **+ Fine-tune a model**
- Base model: `gpt-4o-2024-08-06`
- Upload `train.jsonl` and `validation.jsonl`

**2. Configure hyperparameters**

| Parameter | Value | Notes |
|---|---|---|
| Epochs | `3` | Increase to 5 for smaller datasets |
| Batch size | `auto` | Azure-managed |
| Learning rate multiplier | `1.0` | Raise to 2.0 if loss plateaus |
| Model suffix | `project-demo` | Appears in deployment name |

> 💰 **Estimated cost:** 400 examples × ~150 tokens × 3 epochs ≈ 180K tokens ≈ **$4.50**

**3. Monitor the job**

```
Queued → Running → Succeeded ✅  (~30–90 minutes)
```

**4. Deploy the model**
- Click **Deploy** on the succeeded model
- Deployment name: `gpt-4o-2024-08-06-project-demo`
- Copy **Endpoint URL** and **API Key** from the Keys & Endpoint panel

**5. Test in Playground**
- Azure AI Foundry → **Playground** → **Chat**
- Select your fine-tuned deployment
- Verify the model responds in the trained support persona

---

## 💬 Phase 3 · React Chat Application

The chat UI connects **directly** to Azure OpenAI with SSE streaming — no backend required for the frontend-only deployment.

### Running Locally

```bash
npm install
npm run dev              # Vite dev server → http://localhost:5173
```

### Production Build

```bash
npm run build            # Output → ./dist/
npm run preview          # Preview production build
```

### Configuration Modal

On first launch, a configuration modal prompts for:

| Field | Required | Example |
|---|---|---|
| API Key | ✅ | `sk-xxxxxxxxxxxx` |
| Azure Endpoint | ✅ | `https://resource.cognitiveservices.azure.com/` |
| Deployment Name | ✅ | `gpt-4o-2024-08-06-project-demo` |
| Bot Name | ❌ | `Support Assistant` |
| System Prompt | ❌ | Custom persona instructions |

All credentials are stored in `localStorage` — never transmitted anywhere except directly to Azure.

### Key Features

- **Real-time SSE streaming** — token-by-token response rendering
- **Multi-session sidebar** — persistent conversation history
- **Auto-titling** — sessions named from first user message
- **Typing indicator** — animated dots while streaming initialises
- **Connection test** — one-click API validation before saving
- **Responsive design** — mobile-optimised layout
- **Dark mode design system** — custom CSS variables throughout

### Optional Express Backend

For environments where CORS restrictions prevent direct browser calls:

```bash
cd server
npm install
npm start                # Express proxy → http://localhost:3001
```

The server exposes `POST /api/chat` with SSE streaming and a `GET /health` check.

---

## 🚀 Phase 4 · AWS CI/CD Deployment

### Pipeline Overview

```
git push → GitHub Webhook → CodePipeline triggered
                                    │
                          ┌─────────▼─────────┐
                          │   Source Stage     │
                          │  (GitHub checkout) │
                          └─────────┬─────────┘
                                    │
                          ┌─────────▼─────────┐
                          │   Build Stage      │
                          │  (CodeBuild)       │
                          │  npm ci            │
                          │  npm run build     │
                          └─────────┬─────────┘
                                    │
                          ┌─────────▼─────────┐
                          │   Deploy Stage     │
                          │  (S3 Upload)       │
                          │  Extract files     │
                          │  → Public URL ✅   │
                          └───────────────────┘
```

### `buildspec.yml`

```yaml
version: 0.2

phases:
  install:
    runtime-versions:
      nodejs: 18
    commands:
      - npm ci --legacy-peer-deps

  build:
    commands:
      - npm run build

  post_build:
    commands:
      - echo Build complete.

artifacts:
  files:
    - '**/*'
  base-directory: dist
  discard-paths: no
```

### AWS Setup Checklist

- [ ] Create S3 bucket: `my-react-cicd-demo` (unique name)
- [ ] Create CodePipeline: `reactapp-cicd-demo`
  - Source → GitHub (Version 2), branch `main`
  - Build → CodeBuild project `react-cicd-pipeline-demo`
  - Deploy → S3 bucket, **extract files enabled**
- [ ] Enable S3 Static Website Hosting (`index.html` as index + error document)
- [ ] Unblock public access on the bucket
- [ ] Apply bucket policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-react-cicd-demo/*"
  }]
}
```

- [ ] (Optional) Create CloudFront distribution for HTTPS + CDN

### Testing the Pipeline

```bash
# Make any change, then:
git add .
git commit -m "chore: trigger deployment"
git push origin main

# Watch in AWS Console:
# Source ✅ → Build ✅ → Deploy ✅ (~3–5 min)
```

---

## 🔐 Environment Variables

### Python (Data Generation)

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ | Groq API key from [console.groq.com](https://console.groq.com) |

### React App (Runtime — stored in `localStorage`)

| Field | Required | Description |
|---|---|---|
| Azure API Key | ✅ | Azure OpenAI resource key |
| Azure Endpoint | ✅ | Resource endpoint URL |
| Deployment Name | ✅ | Fine-tuned model deployment name |

### Express Server (Optional)

```env
PORT=3001
```

---

## 📡 API Reference

### Express Proxy — `POST /api/chat`

**Request body:**

```json
{
  "messages":     [{"role": "user", "content": "Hello"}],
  "apiKey":       "your-azure-key",
  "endpoint":     "https://resource.cognitiveservices.azure.com/",
  "deployment":   "gpt-4o-2024-08-06-project-demo",
  "systemPrompt": "You are a helpful support assistant."
}
```

**Response:** `text/event-stream` (SSE)

```
data: {"content": "Hello"}
data: {"content": "! How"}
data: {"content": " can I help?"}
data: [DONE]
```

**Error response:**

```json
{"error": "Missing apiKey, endpoint, or deployment"}
```

### Express Health Check — `GET /health`

```json
{"status": "ok"}
```

---

## 📋 Dataset Format

Azure OpenAI fine-tuning requires **JSONL** with the chat messages format. Each line is a self-contained conversation:

```jsonl
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

### Validation Rules

| Rule | Requirement |
|---|---|
| File format | `.jsonl` — one JSON object per line |
| Required roles | `system`, `user`, `assistant` in each example |
| Token limit | < 4,096 tokens per example |
| Minimum examples | ≥ 10 for training, ≥ 1 for validation |
| Encoding | UTF-8 |

---

## 🧹 Clean Up Resources

To avoid ongoing cloud charges:

**AWS:**
```
CodePipeline  → Delete: reactapp-cicd-demo
CodeBuild     → Delete: react-cicd-pipeline-demo
S3            → Empty bucket → Delete: my-react-cicd-demo
CloudFront    → Disable + Delete distribution (if created)
IAM           → Remove auto-generated service roles (optional)
```

**Azure:**
```
AI Foundry    → Delete fine-tuned model deployment
              → Delete fine-tuning job
Azure OpenAI  → Delete resource (if no longer needed)
```

---

## 🤝 Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit with a conventional message: `git commit -m "feat: add your feature"`
4. Push and open a Pull Request

Please ensure:
- New Python code follows the LangChain 1.2.0 LCEL pattern
- React components are functional with hooks
- No hardcoded API keys or credentials

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with LangChain 1.2.0 · Azure AI Foundry · AWS CodePipeline · React 19**

<br />

<img src="https://img.shields.io/badge/Made%20with-Python-3776AB?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Powered%20by-Groq-F55036?style=flat-square" />
<img src="https://img.shields.io/badge/Deployed%20on-AWS%20S3-FF9900?style=flat-square&logo=amazons3&logoColor=white" />
<img src="https://img.shields.io/badge/Model%20on-Azure-0078D4?style=flat-square&logo=microsoftazure&logoColor=white" />

</div>
