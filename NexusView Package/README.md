# NexusViewPro 🚀

[![PyPI version](https://img.shields.io/pypi/v/NexusViewPro.svg)](https://pypi.org/project/NexusViewPro/)
[![Python versions](https://img.shields.io/pypi/pyversions/NexusViewPro.svg)](https://pypi.org/project/NexusViewPro/)
[![License](https://img.shields.io/pypi/l/NexusViewPro.svg)](https://github.com/entbappy/NexusViewPro/blob/main/LICENSE)
[![CI](https://github.com/entbappy/NexusViewPro/actions/workflows/ci.yml/badge.svg)](https://github.com/entbappy/NexusViewPro/actions/workflows/ci.yml)

**NexusViewPro** is a lightweight Python library for Data Scientists and notebook users. It lets you render live websites and embed YouTube videos directly inside Jupyter Notebook, JupyterLab, and Google Colab — without leaving your environment.

---

## Features

- **Website Rendering** — Display any HTTPS page in an output cell via a resizable IFrame.
- **YouTube Embedding** — Automatically parses standard and shortened YouTube URLs and renders the video player inline.
- **Customisable Viewport** — Control `width` and `height` of any rendered element.
- **Structured Logging** — Built-in logger writes to both stdout and `logs/running_logs.log`.
- **Lightweight** — No heavy dependencies; built entirely on top of standard IPython display utilities.

---

## Installation

```bash
pip install NexusViewPro
```

---

## Quick Start

**Embed a YouTube video:**

```python
from NexusViewPro.youtube import render_youtube_video

render_youtube_video("https://www.youtube.com/watch?v=h25pePMdoPA&t=712s")
```

**Render a website:**

```python
from NexusViewPro.site import render_site

render_site("https://example.com", width="100%", height="600")
```

---

## Project Structure

```
NexusViewPro/
├── src/
│   └── NexusViewPro/
│       ├── __init__.py
│       ├── logger.py            # Structured logger (file + stdout)
│       ├── custom_exception.py  # InvalidURLException
│       ├── site.py              # render_site()
│       └── youtube.py           # render_youtube_video()
├── tests/
│   ├── unit/
│   └── integration/
├── logs/
├── setup.py
├── setup.cfg
├── pyproject.toml
├── requirements.txt
├── requirements_dev.txt
└── tox.ini
```

---

## Development Setup

```bash
conda create -n nexusviewpro_env python=3.8 -y
conda activate nexusviewpro_env
pip install -r requirements_dev.txt
```

This installs the package in editable mode (`-e .`) along with all dev dependencies (pytest, flake8, mypy, tox).

**Run tests:**

```bash
pytest -v tests/
```

**Run the full lint + type-check + test suite:**

```bash
tox
```

---

## Google Colab

A self-contained notebook (`NexusViewPro_Colab.ipynb`) is included. It recreates the project structure, installs dependencies, runs all demos, executes the test suite, and exports the project as a `.zip` for download — all in sequence with saved cell outputs.

Open directly in Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/entbappy/NexusViewPro/blob/main/NexusViewPro_Colab.ipynb)

---

## API Reference

### `render_youtube_video(url, width=780, height=440)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | `str` | — | Any standard YouTube URL (`watch?v=`, `youtu.be/`, etc.) |
| `width` | `int` | `780` | IFrame width in pixels |
| `height` | `int` | `440` | IFrame height in pixels |

Raises `InvalidURLException` if no valid video ID can be extracted from the URL.

---

### `render_site(URL, width="100%", height="600")`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `URL` | `str` | — | A reachable HTTPS URL |
| `width` | `str` | `"100%"` | IFrame width (CSS value) |
| `height` | `str` | `"600"` | IFrame height in pixels |

Raises `InvalidURLException` if the URL returns a non-200 status or is unreachable.

> **Note:** Some sites block iframe embedding via `X-Frame-Options`. This is a server-side restriction and not a library limitation.

---

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.
