# 🤖 AI-Powered Resume & Job Analyzer

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangChain-🦜-121011?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/OpenAI-GPT-412991?style=for-the-badge&logo=openai&logoColor=white"/>
  <img src="https://img.shields.io/badge/Groq-LPU-F55036?style=for-the-badge"/>
</p>

<p align="center">
  An intelligent, AI-driven web application that analyzes your resume against any job description — providing ATS scoring, skill gap detection, and personalized improvement suggestions powered by Large Language Models.
</p>

---

## 📌 Overview

Job hunting is competitive. Recruiters spend mere seconds scanning a resume, and most applications never even reach a human — they're filtered out by Applicant Tracking Systems (ATS) first.

**AI-Powered Resume & Job Analyzer** bridges that gap. Upload your resume and paste a job description, and the app instantly tells you how well you match, what skills you're missing, and exactly how to improve your resume for that specific role — all powered by LLMs via LangChain and Groq/OpenAI.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **Resume Parsing & Skill Extraction** | Automatically extracts skills, experience, education, and key information from your uploaded resume (PDF/text) |
| 🔍 **Job Description Analysis** | Parses the target job posting to identify required skills, qualifications, and keywords |
| 📊 **ATS Score / Match Percentage** | Calculates a compatibility score showing how well your resume aligns with the job description |
| 💡 **AI-Generated Improvement Suggestions** | Provides actionable, role-specific recommendations to strengthen your resume and close skill gaps |

---

## 🛠️ Tech Stack

- **Language:** Python 3.9+
- **Framework:** Streamlit (interactive web UI)
- **LLM Orchestration:** LangChain
- **LLM Providers:** Groq (LLaMA / Mixtral) and/or OpenAI (GPT-3.5 / GPT-4)
- **Document Parsing:** PyPDF2 / pdfplumber
- **Environment Management:** python-dotenv

---

## 📂 Project Structure

```
ai-resume-job-analyzer/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
│
├── utils/
│   ├── parser.py           # Resume & JD parsing logic
│   ├── analyzer.py         # ATS scoring and matching
│   └── llm_chain.py        # LangChain prompt chains
│
└── prompts/
    └── templates.py        # LLM prompt templates
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- An API key from [OpenAI](https://platform.openai.com/) and/or [Groq](https://console.groq.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-resume-job-analyzer.git
cd ai-resume-job-analyzer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the Application

```bash
streamlit run app.py
```

Open your browser and navigate to `http://localhost:8501`.

---

## 🧠 How It Works

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   1. Upload Resume (PDF)  ──►  Parse & Extract Skills        │
│                                                              │
│   2. Paste Job Description ──►  Identify Requirements        │
│                                                              │
│   3. LangChain + LLM  ──►  Compare & Score (ATS Match %)     │
│                                                              │
│   4. Generate Report  ──►  Gaps + Suggestions + Score        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

1. **Parse** — The resume is extracted and cleaned using PDF parsing libraries.
2. **Analyze** — LangChain orchestrates prompts to compare resume content against the job description.
3. **Score** — An ATS compatibility percentage is computed based on keyword and skill overlap.
4. **Suggest** — The LLM generates tailored recommendations to improve the resume for the specific role.

---

## 📸 Demo

> *(Add a screenshot or screen recording of the app here)*

```
[Screenshot Placeholder]
```

---

## 📋 Requirements

```txt
streamlit
langchain
langchain-openai
langchain-groq
openai
groq
pypdf2
pdfplumber
python-dotenv
```

Install all with:

```bash
pip install -r requirements.txt
```

---

## 🔑 API Keys

This project supports two LLM backends — you can use either or both:

| Provider | Get API Key | Free Tier |
|---|---|---|
| OpenAI | https://platform.openai.com/api-keys | Limited free credits |
| Groq | https://console.groq.com/ | Generous free tier |

> 💡 **Tip:** Groq offers extremely fast inference for free — great for testing and demos.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve this project:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to your branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [your-linkedin](https://linkedin.com/in/your-linkedin)

---

## ⭐ Show Your Support

If you found this project helpful, please consider giving it a ⭐ on GitHub — it means a lot!

---

> *Built with ❤️ using Python, LangChain, and Streamlit*
