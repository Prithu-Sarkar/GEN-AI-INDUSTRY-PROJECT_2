# 📝 Text Summarization with Hugging Face Transformers

An end-to-end NLP pipeline that fine-tunes **Google's PEGASUS** model on the **SAMSum** dialogue dataset for abstractive text summarization. The project is structured as a modular, production-style ML system with a FastAPI inference server and a fully self-contained Google Colab notebook.

---

## 🌟 Features

- Fine-tunes `google/pegasus-cnn_dailymail` on the SAMSum conversational dataset
- Modular pipeline architecture: each stage is independently runnable
- ROUGE metric evaluation (ROUGE-1, ROUGE-2, ROUGE-L, ROUGE-Lsum)
- FastAPI REST API for training triggers and real-time inference
- Groq LLM integration (`llama-3.1-8b-instant`) for fast zero-shot summarization
- Google Colab notebook — fully self-contained, no local setup required
- All outputs zipped for easy download from Colab

---

## 🏗️ Project Structure

```
TextSummarizer/
│
├── config/
│   └── config.yaml                   # Pipeline paths and model checkpoints
│
├── src/textSummarizer/
│   ├── components/
│   │   ├── data_ingestion.py         # Dataset download and extraction
│   │   ├── data_transformation.py    # Tokenization with PEGASUS tokenizer
│   │   ├── model_trainer.py          # Fine-tuning with HuggingFace Trainer
│   │   └── model_evaluation.py       # ROUGE score computation
│   │
│   ├── config/
│   │   └── configuration.py          # ConfigurationManager: reads YAMLs, returns typed configs
│   │
│   ├── constants/
│   │   └── __init__.py               # Config file paths
│   │
│   ├── entity/
│   │   └── __init__.py               # Dataclasses for each stage's config
│   │
│   ├── logging/
│   │   └── __init__.py               # Centralised logger (file + stdout)
│   │
│   ├── pipeline/
│   │   ├── stage_1_data_ingestion_pipeline.py
│   │   ├── stage_2_data_transformation_pipeline.py
│   │   ├── stage_3_model_trainer_pipeline.py
│   │   ├── stage_4_model_evaluation.py
│   │   └── prediction_pipeline.py    # Inference wrapper
│   │
│   └── utils/
│       └── common.py                 # YAML loader, directory creator
│
├── research/
│   ├── 1_data_ingestion.ipynb
│   ├── 2_data_transformation.ipynb
│   ├── 3_model_trainer.ipynb
│   ├── 4_model_evaluation.ipynb
│   └── textsummarizer.ipynb          # Full exploratory notebook
│
├── artifacts/                        # Generated at runtime (gitignored)
│   ├── data_ingestion/
│   ├── data_transformation/
│   ├── model_trainer/
│   └── model_evaluation/
│
├── logs/                             # Runtime logs (gitignored)
├── app.py                            # FastAPI application
├── main.py                           # CLI entry point (runs all 4 stages)
├── params.yaml                       # Training hyperparameters
├── requirements.txt
├── setup.py
└── Text_Summarization_Colab.ipynb    # ⭐ Self-contained Colab notebook
```

---

## 🔄 Pipeline Stages

```
Stage 1            Stage 2               Stage 3             Stage 4
─────────────      ─────────────────     ───────────────     ─────────────────
Data Ingestion  →  Data               →  Model           →  Model
                   Transformation        Training            Evaluation
Download &         Tokenize with         Fine-tune           Compute ROUGE
extract SAMSum     PEGASUS tokenizer     PEGASUS on          scores on test
dataset            Save Arrow format     SAMSum              set → CSV
```

---

## 🚀 Quick Start

### Option A — Google Colab (Recommended)

1. Open `Text_Summarization_Colab.ipynb` in Google Colab
2. Set runtime to **GPU** (T4): *Runtime → Change runtime type → T4 GPU*
3. Add secrets in the left sidebar (🔑):
   - `GROQ_API_KEY` — from [console.groq.com](https://console.groq.com)
   - `NGROK_AUTHTOKEN` — from [dashboard.ngrok.com](https://dashboard.ngrok.com) *(optional, for API serving)*
4. Run all cells: *Runtime → Run all*

### Option B — Local Setup

**Prerequisites:** Python 3.10+, CUDA-capable GPU recommended

```bash
# 1. Clone the repository
git clone https://github.com/your-username/text-summarizer.git
cd text-summarizer

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -e .                # installs the src package in editable mode

# 4. Run the full pipeline
python main.py
```

---

## ⚙️ Configuration

### `config/config.yaml`

Controls all file paths and the base model checkpoint:

```yaml
data_ingestion:
  source_URL: https://github.com/krishnaik06/datasets/raw/refs/heads/main/summarizer-data.zip

data_transformation:
  tokenizer_name: google/pegasus-cnn_dailymail

model_trainer:
  model_ckpt: google/pegasus-cnn_dailymail

model_evaluation:
  metric_file_name: artifacts/model_evaluation/metrics.csv
```

### `params.yaml`

Training hyperparameters — edit here to tune without touching code:

```yaml
TrainingArguments:
  num_train_epochs: 1
  warmup_steps: 500
  per_device_train_batch_size: 1
  weight_decay: 0.01
  logging_steps: 10
  evaluation_strategy: steps
  eval_steps: 500
  save_steps: 1000000
  gradient_accumulation_steps: 16
```

---

## 🌐 API Reference

Start the server locally:

```bash
python app.py
# Server runs at http://0.0.0.0:8080
# Interactive docs at http://localhost:8080/docs
```

| Method | Endpoint   | Description                              |
|--------|------------|------------------------------------------|
| GET    | `/`        | Redirects to Swagger UI (`/docs`)        |
| GET    | `/train`   | Triggers the full 4-stage training pipeline |
| POST   | `/predict` | Summarises the provided `text` parameter |

**Example prediction request:**

```bash
curl -X POST "http://localhost:8080/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hannah: Are you coming tonight? Eric: Maybe, I need to finish work first."}'
```

**Response:**

```json
{
  "summary": "Eric may join Hannah tonight after finishing work."
}
```

---

## ⚡ Groq LLM Integration

This project includes a fast zero-shot summarization path using **Groq's `llama-3.1-8b-instant`** model — no fine-tuning or GPU required.

```python
from groq import Groq

client = Groq(api_key="YOUR_GROQ_API_KEY")

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "Summarise the following dialogue concisely."},
        {"role": "user",   "content": "Hannah: Hey, are you free tonight? ..."}
    ]
)

print(response.choices[0].message.content)
```

In Colab, store the key under **Secrets → `GROQ_API_KEY`** — it is read via `google.colab.userdata` and never written to notebook outputs.

---

## 📊 Model & Dataset

| Item | Detail |
|------|--------|
| Base model | [`google/pegasus-cnn_dailymail`](https://huggingface.co/google/pegasus-cnn_dailymail) |
| Dataset | [SAMSum](https://huggingface.co/datasets/samsum) — 16,369 messenger-style dialogues |
| Task | Abstractive summarization (seq2seq) |
| Tokenizer | PEGASUS SentencePiece tokenizer |
| Max input length | 1,024 tokens |
| Max summary length | 128 tokens |
| Evaluation metric | ROUGE-1, ROUGE-2, ROUGE-L, ROUGE-Lsum |

---

## 📦 Artifacts

After running the pipeline the following are generated (all gitignored):

```
artifacts/
├── data_ingestion/
│   ├── data.zip
│   └── samsum_dataset/          # HuggingFace Arrow dataset
├── data_transformation/
│   └── samsum_dataset/          # Tokenized Arrow dataset
├── model_trainer/
│   ├── pegasus-samsum-model/    # Fine-tuned model weights
│   └── tokenizer/               # Saved tokenizer
└── model_evaluation/
    └── metrics.csv              # ROUGE scores
```

In Colab, Phase 9 of the notebook zips everything into `text_summarizer_outputs.zip` and triggers a browser download.

---

## 🔧 Dependencies

| Package | Purpose |
|---------|---------|
| `transformers` | PEGASUS model, tokenizer, Trainer |
| `datasets` | SAMSum loading and Arrow serialization |
| `evaluate` | ROUGE metric computation |
| `torch` | Deep learning backend |
| `groq` | Groq LLM API client |
| `fastapi` + `uvicorn` | REST API server |
| `python-box` | Dot-access config dictionaries |
| `ensure` | Runtime type annotation enforcement |
| `PyYAML` | YAML config parsing |
| `pandas` | Metrics CSV export |
| `pyngrok` | ngrok tunnel for Colab API serving |

---

## 📋 Requirements

```
Python >= 3.10
CUDA-capable GPU (recommended for training; T4 on Colab works well)
~10 GB disk space for model weights + dataset
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [Google Research](https://ai.googleblog.com/2020/06/pegasus-state-of-art-model-for.html) for the PEGASUS model
- [HuggingFace](https://huggingface.co) for the Transformers and Datasets libraries
- [Samsung Research](https://arxiv.org/abs/1911.12237) for the SAMSum dataset
- [Groq](https://groq.com) for ultra-fast LLM inference
