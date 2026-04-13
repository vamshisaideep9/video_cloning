# Video Cloning Platform - Architecture & Technical Specification

## 1. System Overview
A resource-efficient, zero-cost (infrastructure-aside), CPU-bound video cloning and lip-syncing API. The system ingests a source image/video and target audio (or text for TTS), processes the heavy ML workloads asynchronously via a message queue, and tracks performance metrics via remote MLflow.

## 2. Technology Stack
* **Backend Framework**: FastAPI (Asynchronous, Type-hinted, PEP 8)
* **Package Manager**: `uv` (for ultra-fast dependency resolution)
* **Database**: PostgreSQL (Relational metadata, Job states)
* **Task Queue**: Celery + Redis
* **ML Tracking**: MLflow (Hosted on DagsHub - 0 Cost)
* **Containerization**: Docker & Docker Compose (Multi-stage builds)

## 3. ML Pipeline Strategy (CPU-Optimized)
To maintain high efficiency and sub-8GB memory constraints on CPU:
* **Audio Generation (TTS/Voice Cloning)**: **F5-TTS**. Highly efficient zero-shot voice cloning. We will export the model to ONNX or use OpenVINO for CPU acceleration.
* **Video Animation/Lip-Sync**: **LivePortrait**. Extremely fast, lightweight. We will utilize the ONNX CPU runtime.
* **Optimization Tactics**: INT8 Quantization, batch size of 1, limiting thread usage (`OMP_NUM_THREADS=4`), and dropping all `torch` CUDA dependencies from `requirements.txt`.

## 4. System Architecture Flow
1.  **Client** submits `source_image` and `target_audio` to FastAPI `/api/v1/clone`.
2.  **FastAPI** writes a `PENDING` job to **PostgreSQL** and publishes the task to **Redis**.
3.  **FastAPI** returns the `job_id` to the client.
4.  **Celery Worker** picks up the task from Redis.
5.  **Celery Worker** triggers the ML Engine:
    * MLflow run starts (tracking via DagsHub).
    * F5-TTS processes audio (if TTS is needed).
    * LivePortrait aligns the face and generates the frames.
    * FFmpeg multiplexes the generated video with the target audio.
6.  **Celery Worker** uploads/saves the artifact, updates **PostgreSQL** to `COMPLETED`, and logs execution time to **DagsHub**.

## 5. Core Database Schema (PostgreSQL)
Table: `cloning_jobs`
* `id` (UUID, Primary Key)
* `status` (Enum: PENDING, PROCESSING, COMPLETED, FAILED)
* `source_file_path` (String)
* `audio_file_path` (String)
* `result_file_path` (String, Nullable)
* `error_logs` (Text, Nullable)
* `created_at` (Timestamp)
* `updated_at` (Timestamp)

## 6. REST API Endpoints
* `POST /api/v1/jobs/` - Create a new video cloning task (Upload files). Returns Job ID.
* `GET /api/v1/jobs/{job_id}` - Poll task status.
* `GET /api/v1/jobs/{job_id}/download` - Retrieve the finalized MP4.
* `GET /health` - System health check (DB, Redis, Worker status).

## 7. DevOps & Deployment Standards
* **Docker Strategy**: Use `python:3.11-slim`. Build C++ dependencies in a builder stage and copy only compiled binaries and the `.venv` to the runtime image.
* **Environment Variables**: Strictly managed via `.env` (Database credentials, DagsHub tokens).