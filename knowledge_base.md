# Video Cloning Platform - Knowledge Base & State Checkpoint

## 1. Project Mission & Constraints
* **Goal**: Build a resource-efficient, asynchronous video cloning and lip-syncing API.
* **Constraints**: 
  * STRICTLY CPU-bound (0 cloud GPU costs). 
  * RAM footprint < 8GB. 
  * Open-source models only.
* **Core ML Engine**:
  * Voice Cloning: **F5-TTS** (ONNX/OpenVINO CPU execution).
  * Video/Lip-Sync: **LivePortrait** (ONNX CPU execution).

## 2. Technology Stack
* **API**: FastAPI (Async) + Uvicorn
* **Dependency Manager**: `uv` (Strictly using PyTorch CPU indices)
* **Task Queue**: Celery + Redis
* **Database**: PostgreSQL + SQLAlchemy 2.0 (Asyncpg for FastAPI, Psycopg2 for Celery)
* **Telemetry/MLOps**: DagsHub (MLflow remote server)
* **Containerization**: Docker + Docker Compose (Multi-stage builds)

## 3. Directory Structure
```text
video_clone_project/
├── app/
│   ├── api/             # FastAPI Endpoints
│   ├── core/            # Config, DB, Celery Setup
│   ├── models/          # SQLAlchemy ORM Models
│   └── services/        # ML Inference & Tracking Singletons
├── .env                 # Environment variables
├── docker-compose.yml   # Services: API, DB, Redis, Worker
├── Dockerfile           # Multi-stage uv-optimized image
├── pyproject.toml       # Dependencies (CPU-bound)
└── knowledge_base.md    # THIS FILE
4. Current Implementation State (Checkpoint: DB & Config Ready)
Completed Components:

pyproject.toml: Configured with uv. extra-index-url pointing to download.pytorch.org/whl/cpu is active.

Dockerfile: Multi-stage build using ghcr.io/astral-sh/uv:latest to cache layers and install ffmpeg.

docker-compose.yml: API service configured.

app/core/config.py: Pydantic BaseSettings reading from .env (Postgres, Redis, DagsHub credentials).

app/core/database.py: Async engine configuration with asyncpg and dependency injection (get_db).

app/models/job.py: Defined CloningJob table tracking states: PENDING, PROCESSING, COMPLETED, FAILED.

app/main.py: Initialized with /health route and lifespan context manager to run Base.metadata.create_all.

5. Next Steps / Pending Tasks
Infrastructure: Add postgres and redis services to docker-compose.yml.

Message Broker: Write app/core/celery_app.py to configure the worker.

API Routes: Implement POST /api/v1/clone to ingest images/audio, create DB records, and dispatch Celery tasks.

ML Integration: Implement the F5-TTS CPU inference wrapper in app/services/.

6. Operational Protocol for LLM
Assume the files listed in Section 4 are complete and correctly configured.

Do NOT introduce CUDA (cu118, cu121) dependencies.

Maintain the Senior Lead Engineer persona: Provide Impact Analysis, Architecture Map, and Draft Plans before outputting code. No fluff.