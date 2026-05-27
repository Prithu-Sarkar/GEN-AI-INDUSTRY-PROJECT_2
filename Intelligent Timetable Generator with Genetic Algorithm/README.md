<div align="center">

<!-- Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0c29,50:302b63,100:24243e&height=200&section=header&text=Intelligent%20Timetable%20Generator&fontSize=38&fontColor=ffffff&fontAlignY=38&desc=Genetic%20Algorithm%20%E2%80%A2%20Flask%20%E2%80%A2%20Gradio%20%E2%80%A2%20SQLite&descAlignY=58&descSize=16&animation=fadeIn" width="100%"/>

<!-- Badges -->
<p>
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-2.3%2B-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gradio-4.0%2B-F97316?style=for-the-badge&logo=gradio&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
  <img src="https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white"/>
</p>

<p>
  <img src="https://img.shields.io/badge/Algorithm-Genetic-8B5CF6?style=flat-square"/>
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=flat-square"/>
  <img src="https://img.shields.io/badge/Status-Production%20Ready-22C55E?style=flat-square"/>
  <img src="https://img.shields.io/badge/Notebook-Colab%20Compatible-F9AB00?style=flat-square&logo=googlecolab&logoColor=white"/>
</p>

<br/>

> **An automated academic scheduling system that harnesses the power of evolutionary computation  
> to generate conflict-free, optimised timetables — in seconds.**

<br/>

[**Explore the Notebook**](#-notebook-phases) · [**API Reference**](#-api-reference) · [**Quick Start**](#-quick-start) · [**Architecture**](#-architecture)

</div>

---

## ✦ What This Project Does

Managing academic timetables is an **NP-hard combinatorial optimisation problem**.  
Manual scheduling for even a mid-size institution can take days and still produce conflicts.

This system solves it **automatically** using a **Genetic Algorithm** that:

- 📌 Respects hard constraints — no teacher double-booking, no break-time classes
- 🎯 Optimises soft constraints — subject priority, consecutive double-lecture blocks, daily variety
- ⚡ Runs in seconds — population-based search with configurable depth
- 💾 Persists results — SQLite database, no server required
- 🌐 Exposes two interfaces — a REST API (Flask) and an interactive UI (Gradio)

---

## 🗂 Project Structure

```
Intelligent-Timetable-Generator/
│
├── 📓  Intelligent_Timetable_Generator.ipynb   ← Main notebook (all 7 phases)
│
├── 🐍  app.py                                  ← Flask application entry point
│
├── 📦  src/
│   ├── auth/           auth.py                 ← Session-based authentication
│   ├── database/       database.py             ← SQLite connection & CRUD helpers
│   ├── logic/          algorithms.py           ← Genetic Algorithm engine
│   │                   config.py               ← App-wide configuration
│   ├── routes/         generation.py           ← /generate endpoint
│   │                   management.py           ← CRUD routes (teachers, subjects…)
│   │                   timetable.py            ← Timetable view & export
│   │                   main.py                 ← Auth & dashboard routes
│   ├── services/       timetable_service.py    ← Business-logic orchestration
│   └── utils/          decorators.py           ← login_required + helpers
│
├── 🎨  frontend/
│   ├── templates/      *.html                  ← Jinja2 page templates (15 pages)
│   └── static/         style.css  script.js    ← CSS & JavaScript assets
│
├── 🗄  sql/
│   ├── schema.sql                              ← Full DB schema (MySQL + SQLite)
│   ├── run_queries.sql                         ← Operational queries
│   └── practice_queries.sql                   ← Learning & exploration queries
│
├── requirements.txt
└── .env.example
```

---

## 🧬 The Genetic Algorithm

The scheduling engine (`src/logic/algorithms.py`) implements a **custom evolutionary search**:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         GENETIC ALGORITHM FLOW                            │
│                                                                           │
│   INITIALISE                EVALUATE              SELECT                  │
│  ┌──────────┐  candidates  ┌──────────┐  scores  ┌──────────┐           │
│  │ Generate │ ───────────► │ Fitness  │ ────────► │ Keep     │           │
│  │ Pool     │              │ Function │           │ Best     │           │
│  └──────────┘              └──────────┘           └──────────┘           │
│       │                                                │                  │
│       │◄────────────────────────────────────────────── │                  │
│       │          repeat for N attempts                  │                  │
│                                                                           │
│   FITNESS FUNCTION WEIGHTS                                                │
│   ● Subject variety per day      +100 pts each distinct subject           │
│   ● Priority weight bonus        +2 × priority_score per entry            │
│   ● Consecutive double-lecture   +20 × priority (high-priority only)      │
│   ● Over 2 per day penalty       −500 pts per excess lecture              │
│   ● Non-contiguous scatter       −100 × count per subject                 │
└──────────────────────────────────────────────────────────────────────────┘
```

### Constraints Enforced

| Constraint | Type | Mechanism |
|---|---|---|
| Teacher availability | **Hard** | `invalid_slots` map blocks double-bookings |
| Break periods | **Hard** | Break slots excluded from candidate pool |
| Max 2 same-subject/day | **Hard** | `daily_count` guard during candidate generation |
| Consecutive priority blocks | **Soft** | Greedy consecutive-pair placement pass |
| Subject spread across days | **Soft** | Fitness reward for variety |

---

## 🏛 Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          SYSTEM ARCHITECTURE                             │
│                                                                          │
│   ┌─────────────┐     HTTP/JSON      ┌──────────────────────────────┐   │
│   │   Gradio    │ ◄────────────────► │        Flask REST API         │   │
│   │     UI      │   (port 7860)      │         (port 5050)           │   │
│   └─────────────┘                   │                                │   │
│                                     │  /register   /login            │   │
│   ┌─────────────┐                   │  /dashboard                    │   │
│   │   Browser   │ ◄────────────────► │  /manage_teachers             │   │
│   │  (Jinja2    │   HTML templates  │  /manage_classes               │   │
│   │  templates) │                   │  /manage_subjects              │   │
│   └─────────────┘                   │  /generate   /get_timetable    │   │
│                                     └──────────────┬─────────────────┘   │
│                                                    │                     │
│                                     ┌──────────────▼─────────────────┐   │
│                                     │        Service Layer            │   │
│                                     │   timetable_service.py         │   │
│                                     │   • Slot generation             │   │
│                                     │   • Constraint building         │   │
│                                     │   • GA orchestration            │   │
│                                     └──────────────┬─────────────────┘   │
│                                                    │                     │
│                             ┌──────────────────────┤                     │
│                             │                      │                     │
│              ┌──────────────▼────────┐  ┌──────────▼──────────────────┐  │
│              │  Genetic Algorithm    │  │        SQLite Database       │  │
│              │  algorithms.py        │  │                              │  │
│              │  • Fitness function   │  │  schools  teacher  class     │  │
│              │  • Candidate gen      │  │  subject  timeslot room      │  │
│              │  • Selection loop     │  │  timetable  practical        │  │
│              └───────────────────────┘  └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📓 Notebook Phases

The notebook (`Intelligent_Timetable_Generator.ipynb`) is structured as **7 self-contained phases**:

| Phase | Title | Key Output |
|:---:|---|---|
| **1** | Environment Setup | All packages installed, logging configured |
| **2** | Database Layer | SQLite schema created, CRUD helpers defined |
| **3** | Genetic Algorithm Engine | Full GA with fitness function & constraints |
| **4** | Service Layer | Slot generation, orchestration pipeline |
| **5** | Flask REST API | 7 route groups, background thread server |
| **6** | Gradio UI | 8-tab interactive interface |
| **7** | End-to-End Demo | Full pipeline test, timetable pivot table |

> ⚠️ **Notebook Safety**: Built as raw JSON — no `execution_count` artifacts, no checkpoint metadata, no `nbformat` validation errors on push to Git.

---

## ⚡ Quick Start

### Option A — Run the Notebook (Recommended)

```bash
# 1. Clone the repo
git clone https://github.com/your-username/intelligent-timetable-generator.git
cd intelligent-timetable-generator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Open the notebook
jupyter notebook Intelligent_Timetable_Generator.ipynb
# — OR —
# Upload to Google Colab and run all cells
```

Run all cells top-to-bottom. The notebook will:
1. Install all packages
2. Initialise the SQLite database
3. Start Flask on **port 5050** (background thread)
4. Launch Gradio on **port 7860**

---

### Option B — Run the Flask App Standalone

```bash
# Copy and configure environment
cp .env.example .env
# Edit .env: set SECRET_KEY

# Install and launch
pip install -r requirements.txt
python app.py
```

Navigate to `http://localhost:5000`

---

## 🛠 API Reference

All endpoints return JSON. Authentication uses server-side sessions (cookie-based).

### Auth

| Method | Endpoint | Body | Description |
|---|---|---|---|
| `POST` | `/register` | `school_name, username, password, start_time, ...` | Register school admin |
| `POST` | `/login` | `username, password` | Authenticate, start session |
| `POST` | `/logout` | — | Clear session |

### Management

| Method | Endpoint | Body | Description |
|---|---|---|---|
| `GET` | `/manage_teachers` | — | List all teachers |
| `POST` | `/manage_teachers` | `teacher_name` | Add teacher |
| `PUT` | `/manage_teachers/<id>` | `teacher_name` | Update teacher |
| `DELETE` | `/manage_teachers/<id>` | — | Delete teacher + cascade |
| `GET/POST` | `/manage_classes` | `class_name` | List / add classes |
| `GET/POST` | `/manage_subjects` | `subject_name, class_id, ...` | List / add subjects |

### Generation & View

| Method | Endpoint | Body / Params | Description |
|---|---|---|---|
| `POST` | `/generate` | `class_name, semester, priorities{}` | Run GA, persist result |
| `GET` | `/get_timetable` | `?class_name=&semester=` | Fetch saved timetable |
| `GET` | `/dashboard` | — | Stats overview |
| `GET` | `/api/schools` | — | Public school list |
| `GET` | `/health` | — | Service health check |

### Example: Full Workflow

```python
import requests

s = requests.Session()
BASE = 'http://localhost:5050'

# 1 — Register
s.post(f'{BASE}/register', json={
    'school_name': 'Tech University', 'username': 'admin',
    'password': 'secret', 'start_time': '09:00',
    'num_lectures': 6, 'lecture_duration': 60,
    'break_after': 3, 'break_duration': 30
})

# 2 — Login
s.post(f'{BASE}/login', json={'username': 'admin', 'password': 'secret'})

# 3 — Setup data
t = s.post(f'{BASE}/manage_teachers', json={'teacher_name': 'Dr. Smith'}).json()
c = s.post(f'{BASE}/manage_classes',  json={'class_name': 'CS-A'}).json()
s.post(f'{BASE}/manage_subjects', json={
    'subject_name': 'Algorithms', 'class_id': c['class_id'],
    'teacher_id': t['teacher_id'], 'semester': 1, 'credits': 4
})

# 4 — Generate
s.post(f'{BASE}/generate', json={
    'class_name': 'CS-A', 'semester': 1,
    'priorities': {'Algorithms': 5}
})

# 5 — View
timetable = s.get(f'{BASE}/get_timetable',
                  params={'class_name': 'CS-A', 'semester': 1}).json()
```

---

## 🗄 Database Schema

```sql
schools        ── school_id, school_name, username, password_hash,
                  start_time, end_time, lecture_duration, break_*

course         ── course_id, course_name, school_id

class          ── class_id, class_name, school_id

teacher        ── teacher_id, teacher_name, school_id

room           ── room_id, room_name, room_type (lecture | practical), school_id

timeslot       ── time_id, timeslot (HH:MM:SS), type_of_class

subject        ── subject_id, subject_name, class_id, course_id,
                  teacher_id, semester, credits, school_id

timetable      ── timetable_id, teacher_id, subject_id, class_id,
                  course_id, time_id, day, school_id

allocated_     ── allocation_id, teacher_id, subject_id, time_id, school_id
timeslots

practical      ── practical_id, practical_name, time_id, room_id,
                  class_id, school_id
```

> All foreign keys are enforced. `ON DELETE CASCADE` keeps data consistent when a school or class is removed.

---

## 🎛 Configuration

`.env` / environment variables:

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `timetable_dev_secret` | Flask session signing key |
| `DB_PATH` | `./timetable.db` | SQLite file location |

**Time configuration** (set at registration, stored per school):

| Parameter | Description | Example |
|---|---|---|
| `start_time` | First lecture begins | `09:00` |
| `num_lectures` | Lectures per day | `6` |
| `lecture_duration` | Minutes per lecture | `60` |
| `break_after` | Break after lecture # | `3` |
| `break_duration` | Break length (minutes) | `30` |

---

## 🧪 Running the Demo

Phase 7 of the notebook runs a **complete automated test** that:

```
1. Health check             → GET  /health
2. Register demo school     → POST /register
3. Login                    → POST /login
4. Dashboard verification   → GET  /dashboard
5. Add 4 teachers           → POST /manage_teachers  ×4
6. Add class CS-A           → POST /manage_classes
7. Add 5 subjects           → POST /manage_subjects  ×5
8. Generate timetable       → POST /generate
9. Fetch & display result   → GET  /get_timetable
```

Sample output:
```
+──────────────+──────────────────+───────────────────+─────────────────+
│  Time Slot   │     Monday       │      Tuesday      │    Wednesday    │
+──────────────+──────────────────+───────────────────+─────────────────+
│  09:00:00    │   Mathematics    │   Data Structures │  OS             │
│  10:00:00    │   Mathematics    │   Mathematics     │  Networks       │
│  11:00:00    │   Data Struct.   │   OS              │  DBMS           │
│  14:00:00    │   Networks       │   DBMS            │  Mathematics    │
│  15:00:00    │   OS             │   Networks        │  Data Struct.   │
│  16:00:00    │   DBMS           │   Data Struct.    │  OS             │
+──────────────+──────────────────+───────────────────+─────────────────+
```

---

## 🔧 Tech Stack

<table>
<tr>
<td><b>Layer</b></td><td><b>Technology</b></td><td><b>Purpose</b></td>
</tr>
<tr>
<td>Algorithm</td><td>Pure Python</td><td>Custom Genetic Algorithm — no ML frameworks needed</td>
</tr>
<tr>
<td>Database</td><td>SQLite 3</td><td>Embedded, zero-config, runs in any environment</td>
</tr>
<tr>
<td>Backend</td><td>Flask 2.3 + Werkzeug</td><td>REST API, session auth, Jinja2 templating</td>
</tr>
<tr>
<td>Interactive UI</td><td>Gradio 4</td><td>No-code web interface for the full pipeline</td>
</tr>
<tr>
<td>Data Layer</td><td>Pandas + Tabulate</td><td>Timetable formatting & pivot display</td>
</tr>
<tr>
<td>Notebook</td><td>Jupyter / Colab</td><td>End-to-end runnable documentation</td>
</tr>
</table>

---

## 📄 License

This project is licensed under the **MIT License** — see [`LICENSE`](LICENSE) for details.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:24243e,50:302b63,100:0f0c29&height=100&section=footer" width="100%"/>

<p>
  <b>Built with evolutionary intelligence.</b><br/>
  <sub>Genetic Algorithm • Flask • Gradio • SQLite • Jupyter</sub>
</p>

</div>
