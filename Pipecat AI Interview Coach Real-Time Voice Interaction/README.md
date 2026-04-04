# 🎤 Pipecat AI Interview Coach

> A real-time voice-powered AI interview coach built with [Pipecat](https://pipecat.ai). The bot conducts live technical interviews through your browser — listening, responding, and adapting its personality based on a job description you provide.

![Interview Coach Demo](image.png)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
  - [1. Clone the repository](#1-clone-the-repository)
  - [2. Configure environment variables](#2-configure-environment-variables)
  - [3. Run the server](#3-run-the-server)
  - [4. Run the client](#4-run-the-client)
- [Running in Google Colab (No Docker)](#running-in-google-colab-no-docker)
- [API Keys Reference](#api-keys-reference)
- [Configuration](#configuration)
  - [Bot Personality Modes](#bot-personality-modes)
  - [Job Description (JD)](#job-description-jd)
  - [Transport Options](#transport-options)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Pipecat AI Interview Coach is a full-stack, real-time voice application that simulates a technical job interview. You paste in a job description, choose how tough you want the interviewer to be, and connect — the AI bot will interview you over WebRTC audio/video, ask relevant questions, and follow up on your answers in real time.

The bot uses a **Deepgram → Groq → ElevenLabs** pipeline for speech-to-text, language understanding, and text-to-speech respectively, all orchestrated by the [Pipecat](https://pipecat.ai) framework. A robot avatar animation plays while the bot speaks.

---

## Features

- **Real-time voice conversation** — low-latency WebRTC audio using Daily or SmallWebRTC transport
- **Animated robot avatar** — 25-frame sprite animation synced to bot speech
- **JD-aware questioning** — bot tailors questions to the job description you provide
- **Three interviewer personalities** — Friendly, Decent, or Strict
- **Live transcript** — conversation log updates in real time
- **Configurable mid-session** — POST to the config API to update personality/JD without restarting
- **Google Colab support** — full one-notebook setup, no Docker required

---

## Architecture

```
Browser (Vite + Vanilla JS)
    │
    │  WebRTC (Daily or SmallWebRTC)
    ▼
Pipecat Bot Server  (:7860)
    ├── Deepgram STT   — speech → text
    ├── Groq LLM       — text → response
    ├── ElevenLabs TTS — response → speech
    └── Sprite animator — robot avatar frames
    
Config API Server  (:7861)
    └── POST /api/interview-config  — update JD & bot nature
    └── GET  /health                — health check
```

The two servers run in the same Python process (config server on a background thread) but expose separate ports. The front-end saves the interview config before connecting, so the bot always has the latest JD when a session starts.

---

## Project Structure

```
interview_prepration_voice_ai_agent/
│
├── server/
│   ├── assets/                  # Robot sprite frames (robot01.png … robot025.png)
│   ├── bot.py                   # Main Pipecat bot — pipeline, animation, transport
│   ├── config_server.py         # aiohttp config API (port 7861)
│   ├── interview_config.json    # Persisted bot nature + JD (auto-updated by API)
│   ├── pyproject.toml           # Python project dependencies (uv)
│   ├── env.example              # Environment variable template
│   ├── Dockerfile               # Docker build (for self-hosted / cloud deploy)
│   └── pcc-deploy.toml          # Pipecat Cloud deployment spec
│
├── client/
│   ├── src/
│   │   ├── app.js               # VoiceChatClient — WebRTC, UI, event handling
│   │   ├── config.js            # Transport config, createTransport factory
│   │   └── style.css            # Dark-theme UI styles
│   ├── index.html               # Single-page HTML shell
│   ├── package.json             # npm dependencies (Vite, pipecat-ai client SDKs)
│   └── env.example              # Client environment variable template
│
├── Pipecat_AI_Interview_Coach.ipynb  # Google Colab notebook (full setup, no Docker)
├── image.png                    # Project screenshot
└── README.md                    # This file
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Orchestration** | [Pipecat](https://pipecat.ai) |
| **Speech-to-Text** | [Deepgram](https://deepgram.com) |
| **LLM** | [Groq](https://groq.com) (fast inference) |
| **Text-to-Speech** | [ElevenLabs](https://elevenlabs.io) |
| **Transport (WebRTC)** | [Daily](https://daily.co) or SmallWebRTC |
| **VAD** | Silero VAD (local) |
| **Turn detection** | LocalSmartTurnAnalyzerV3 |
| **Server framework** | Python + aiohttp |
| **Client framework** | Vanilla JS + Vite |
| **Package manager** | uv (server) / npm (client) |

---

## Prerequisites

- **Python 3.10+**
- **Node.js 18+** and npm
- API keys for: Deepgram, Groq, ElevenLabs
- API key for Daily *(only if using the Daily transport)*
- A modern browser with WebRTC support (Chrome, Edge, Firefox)

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/interview-coach.git
cd interview-coach
```

### 2. Configure environment variables

```bash
cd server
cp env.example .env
```

Edit `.env` and fill in your keys:

```ini
ELEVENLABS_API_KEY=your_elevenlabs_key
DEEPGRAM_API_KEY=your_deepgram_key
GROQ_API_KEY=your_groq_key
DAILY_API_KEY=your_daily_key          # only needed for Daily transport

CONFIG_SERVER_PORT=7861               # optional, defaults to 7861
CONFIG_SERVER_HOST=0.0.0.0            # optional
ALLOWED_ORIGINS=*                     # CORS — lock down in production
```

For the client:

```bash
cd ../client
cp env.example .env.local
```

```ini
VITE_BOT_START_URL=http://localhost:7860/start
VITE_CONFIG_SERVER_URL=http://localhost:7861
```

### 3. Run the server

**With uv (recommended):**

```bash
cd server
uv sync
uv run bot.py
```

**With pip:**

```bash
cd server
pip install -r requirements.txt   # or: pip install "pipecat-ai[daily,deepgram,elevenlabs,groq,silero,webrtc,runner]" aiohttp loguru python-dotenv Pillow
python bot.py
```

The server starts two listeners:

- `http://localhost:7860` — Pipecat bot / WebRTC signalling
- `http://localhost:7861` — Config REST API

### 4. Run the client

```bash
cd client
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

1. Paste a job description (minimum 50 characters)
2. Select a bot personality
3. Choose a transport (SmallWebRTC works without a Daily key)
4. Click **Connect**
5. Allow microphone access when prompted
6. Start talking — the bot will introduce itself and begin the interview

---

## Running in Google Colab (No Docker)

A fully self-contained Colab notebook is included: **`Pipecat_AI_Interview_Coach.ipynb`**

It handles everything automatically — no local installs, no Docker, no manual file creation.

**Steps:**

1. Upload `Pipecat_AI_Interview_Coach.ipynb` to [Google Colab](https://colab.research.google.com)
2. Open **Cell 3** and fill in your API keys in the form fields
3. Run all cells top-to-bottom (Runtime → Run all)
4. After Checkpoint 7, a public ngrok URL appears — open it in your browser

**What the notebook does:**

| Checkpoint | Action |
|---|---|
| 1 | API key entry with validation |
| 2 | Install all system + Python packages |
| 3 | Write all `.py`, `.js`, `.html`, `.json` files to disk |
| 4 | Open ngrok tunnels for bot server and config API |
| 5 | Generate animated robot avatar frames |
| 6 | Start both back-end servers as background processes |
| 7 | npm install → vite build → serve via ngrok |
| 8 | Print live URLs and process status |
| 9 | Zip all output and download |

> **Note:** Free ngrok accounts allow one region per session. The notebook opens three tunnels (bot, config, client) which requires a free ngrok account — sign up at [ngrok.com](https://ngrok.com).

---

## API Keys Reference

| Key | Service | Where to get it |
|---|---|---|
| `ELEVENLABS_API_KEY` | Text-to-speech voice | [elevenlabs.io](https://elevenlabs.io) → Profile → API Key |
| `DEEPGRAM_API_KEY` | Speech-to-text | [console.deepgram.com](https://console.deepgram.com) |
| `GROQ_API_KEY` | LLM inference | [console.groq.com](https://console.groq.com) |
| `DAILY_API_KEY` | WebRTC rooms (Daily transport only) | [dashboard.daily.co](https://dashboard.daily.co) |
| `NGROK_AUTH_TOKEN` | Public tunnels (Colab only) | [dashboard.ngrok.com](https://dashboard.ngrok.com) |

---

## Configuration

### Bot Personality Modes

The interviewer personality is set via the UI dropdown or by POSTing to the config API:

| Mode | Tone | Behaviour |
|---|---|---|
| `friendly` | Warm, encouraging | Conversational questions, empathetic, positive reinforcement |
| `decent` | Professional, balanced | Fair and neutral, standard interview etiquette (default) |
| `strict` | Formal, demanding | Rigorous questions, high standards, direct feedback |

### Job Description (JD)

The bot reads the JD and asks questions relevant to the role — technical skills, experience, and responsibilities mentioned in the description. The JD is truncated to 1500 characters internally to fit within the context window.

**Via the UI:** paste directly into the text area before clicking Connect.

**Via the API:**

```bash
curl -X POST http://localhost:7861/api/interview-config \
  -H "Content-Type: application/json" \
  -d '{
    "botNature": "strict",
    "jd": "Senior Python Engineer at Acme Corp. Requirements: 5+ years Python..."
  }'
```

### Transport Options

| Transport | When to use |
|---|---|
| **SmallWebRTC** | Local development, no Daily API key needed |
| **Daily** | Production, scalable WebRTC rooms with Daily infrastructure |

---

## How It Works

1. **User connects** — browser signals the Pipecat bot server via the selected transport
2. **Config is sent** — client POSTs the JD and bot nature to the config API before connecting
3. **Pipeline starts** — Pipecat assembles: `transport.input → RTVI → Deepgram STT → LLM context → Groq LLM → ElevenLabs TTS → TalkingAnimation → transport.output`
4. **VAD detects speech** — Silero VAD with `stop_secs=0.2` decides when the user has finished speaking
5. **Turn detection** — `LocalSmartTurnAnalyzerV3` avoids cutting the user off mid-sentence
6. **Bot responds** — Groq generates a reply, ElevenLabs synthesises audio, the robot avatar animates
7. **Session ends** — client disconnects; the pipeline is cancelled cleanly

---

## Troubleshooting

**Microphone not working**
Make sure your browser has microphone permissions for the page. In Chrome: address bar → lock icon → Microphone → Allow.

**`SSL: CERTIFICATE_VERIFY_FAILED` on macOS**

```bash
/Applications/Python\ 3.12/Install\ Certificates.command
```

**Bot server exits immediately**
Tail the log and look for a missing API key error:

```bash
tail -50 /content/interview_coach/logs/bot_server.log   # Colab
# or locally:
python server/bot.py 2>&1 | head -50
```

**ngrok tunnel limit (Colab)**
Free ngrok accounts are limited to 1 active agent and 3 tunnels per session. If you see a `ERR_NGROK_108` error, restart the runtime and try again, or upgrade your ngrok plan.

**`npm run build` fails with module not found**
Delete `node_modules` and reinstall:

```bash
cd client && rm -rf node_modules && npm install && npm run build
```

**Bot answers but no audio in browser**
The audio element is appended to `document.body` dynamically when the bot track starts. Check the browser console for `track-started: Bot audio` in the events panel — if it appears but there is no sound, the browser may have blocked autoplay. Click anywhere on the page first to satisfy the autoplay policy.

---

## Contributing

Pull requests are welcome. For significant changes, open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request

Please make sure server-side code passes `ruff check` before submitting:

```bash
cd server && uvx ruff check .
```

---

## License

BSD 2-Clause License. See [LICENSE](LICENSE) for details.

---

*Built with [Pipecat](https://pipecat.ai) — the open-source framework for real-time voice and multimodal AI agents.*
