# LOKTANTRA: The Sovereign Saga

> **A production-grade, cloud-native interactive election simulator for India.** 
> Teaches civic literacy through 8 gamified levels grounded in ECI Constitutional principles (Articles 324-329).

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Powered-4285F4.svg)](https://cloud.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![WCAG 2.1](https://img.shields.io/badge/WCAG-2.1%20AA-brightgreen.svg)](https://www.w3.org/WAI/WCAG21/quickref/)

---

## Google Cloud APIs Used

This project actively integrates the following **Google Cloud Platform** services:

| Service | Package | Purpose |
|---------|---------|---------|
| **Cloud Firestore** | `google-cloud-firestore` | Global Civic Leaderboard — persistent storage for player scores and level progress |
| **Vertex AI (Gemini 1.5 Pro)** | `google-cloud-aiplatform` | AI Reasoning Engine — generates ECI-grounded constitutional explanations for each level |
| **Cloud Logging** | `google-cloud-logging` | Audit Trail — structured logging of every `level_completed` and `score_submitted` event |
| **Cloud Run** | — | Serverless container hosting with auto-scaling and sub-second cold starts |
| **Cloud Build** | — | CI/CD pipeline for automated testing, building, and deployment |
| **Artifact Registry** | — | Docker image storage for Cloud Run deployments |

---

## Architecture

```
┌─────────────────────────────────┐
│        Browser (Client)         │
│   Tailwind CSS · Game Engine    │
└──────────────┬──────────────────┘
               │ REST API
┌──────────────▼──────────────────┐
│      Google Cloud Run           │
│   Flask + Gunicorn (WSGI)       │
│                                 │
│  ┌──────────┐ ┌──────────────┐  │
│  │  Routes   │ │   Services   │  │
│  │  Layer    │ │   Layer      │  │
│  └──────────┘ └──────┬───────┘  │
└──────────────────────┼──────────┘
               ┌───────┼───────┐
               │       │       │
     ┌─────────▼─┐ ┌───▼───┐ ┌▼──────────┐
     │ Firestore  │ │Vertex │ │  Cloud    │
     │(Leaderboard│ │  AI   │ │ Logging   │
     │ + Progress)│ │Gemini │ │  (Audit)  │
     └────────────┘ └───────┘ └───────────┘
```

---

## Game Levels (8 Total)

### The Voter Saga (Levels 1-4)
| Level | Title | Mechanic | ECI Principle |
|-------|-------|----------|---------------|
| L1 | The Electoral Maze | Search & identify voters vs ghosts | Art. 325 — Non-discrimination in rolls |
| L2 | The Great Silence | Deepfake vs Real news classifier | Model Code of Conduct (48h rule) |
| L3 | The Sacred Booth | 3-step EVM + VVPAT simulation | Art. 324 — Superintendence of elections |
| L4 | The Indelible Mark | Ink application precision game | Art. 326 — One-person-one-vote |

### The Officer Saga (Levels 5-8)
| Level | Title | Mechanic | ECI Principle |
|-------|-------|----------|---------------|
| L5 | The Scrutiny Chamber | Candidate affidavit review | Art. 327 / RPA 1951 — Transparency |
| L6 | The 2km Mandate | Booth placement logistics puzzle | Art. 324 — Democratic access |
| L7 | The Dawn Protocol | Mock poll coordination checklist | Art. 324 — Multi-party trust |
| L8 | The Seal of Integrity | Control Unit security sequence | Art. 324 — Chain of custody |

---

## Fictional Parties

- **The Blue Lotus Party** ✧ — *Wisdom Through Unity*
- **The Golden Gear Party** ⚙ — *Progress Through Industry*
- **The Rising Sun Party** ☀ — *A New Dawn for All*
- **The Eternal Flame Party** ⭐ — *Light That Never Fades*

---

## Quick Start

### Prerequisites
- Python 3.12+
- Google Cloud SDK (optional, for cloud features)

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/LOKTANTRA.git
cd LOKTANTRA

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your settings

# Run the application
python main.py
# → http://localhost:8080
```

### With Google Cloud (Full Features)

```bash
# Set your project ID in .env
GCP_PROJECT_ID=your-project-id
ENABLE_FIRESTORE=true
ENABLE_VERTEX_AI=true
ENABLE_CLOUD_LOGGING=true

# Authenticate
gcloud auth application-default login

# Run
python main.py
```

---

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=term-missing

# Run specific test suite
pytest tests/test_scoring_engine.py -v
```

---

## Deployment

### Docker

```bash
# Build image
docker build -t loktantra .

# Verify image size (<500MB)
docker images loktantra

# Run locally
docker run -p 8080:8080 -e FLASK_ENV=production loktantra
```

### Google Cloud Run

```bash
# Using Cloud Build (recommended)
gcloud builds submit --config=cloudbuild.yaml

# Manual deployment
gcloud run deploy loktantra \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --cpu-boost
```

---

## Project Structure

```
LOKTANTRA/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies (google-cloud-*)
├── Dockerfile                 # Multi-stage optimized build
├── cloudbuild.yaml            # CI/CD pipeline
├── app/
│   ├── __init__.py            # Flask app factory
│   ├── config.py              # Configuration management
│   ├── routes/                # API endpoints
│   ├── services/              # Google Cloud integrations
│   ├── game_engine/           # Level logic & validation
│   ├── templates/             # Jinja2 HTML templates
│   └── static/                # CSS, JS, images
└── tests/                     # Pytest test suites
```

---

## Accessibility (WCAG 2.1 AA)

- ✅ ARIA labels on all interactive elements
- ✅ Keyboard navigation for all game mechanics
- ✅ Skip navigation link
- ✅ `prefers-reduced-motion` media query
- ✅ Color contrast ratio ≥ 4.5:1
- ✅ Screen reader live regions for dynamic updates
- ✅ Semantic HTML5 landmarks
- ✅ Focus management during level transitions

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, Flask 3.0, Gunicorn |
| Frontend | Tailwind CSS v3, Vanilla JavaScript |
| Database | Google Cloud Firestore |
| AI | Vertex AI (Gemini 1.5 Pro) |
| Logging | Google Cloud Logging |
| Hosting | Google Cloud Run |
| CI/CD | Google Cloud Build |
| Testing | Pytest, pytest-cov |
| Container | Docker (multi-stage, <500MB) |

---

## License

MIT License — Built for civic education and democratic engagement.
