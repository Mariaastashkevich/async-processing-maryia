# Async Processing API

An asynchronous data processing API built with FastAPI, Celery, PostgreSQL, and MinIO. This application provides endpoints for managing datasets and processing jobs with background task execution.

## Architecture

The application follows a clean architecture pattern with the following components:

```
┌────────────────────────────────────────────────────────────────┐
│                         FastAPI Application                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Routes     │→ │  Use Cases   │→ │     Services         │  │
│  │  (API Layer) │  │  (Business)  │  │   (Domain Logic)     │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                          ↓                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Repositories (Data Access)                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│                    Background Processing                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Celery Workers                              │  │
│  │  - Job Processing                                        │  │
│  │  - Anomaly Detection                                     │  │
│  │  - Metrics Computation                                   │  │
│  │  - Data Normalization                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Infrastructure Services                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │PostgreSQL│  │  Redis   │  │  MinIO   │  │  Storage │         │
│  │(Database)│  │ (Broker) │  │  (S3)    │  │  (Local) │         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

### Key Components

- **FastAPI**: REST API framework for handling HTTP requests
- **Celery**: Distributed task queue for asynchronous job processing
- **PostgreSQL**: Primary database for storing datasets, jobs, and job events
- **Redis**: Message broker and result backend for Celery
- **MinIO**: S3-compatible object storage for dataset and result files
- **Alembic**: Database migration tool

### Data Flow

1. **Dataset Upload**: Client uploads dataset → Stored in MinIO → Metadata saved to PostgreSQL
2. **Job Creation**: Client creates processing job → Job queued via Celery → Job status tracked in PostgreSQL
3. **Job Processing**: Celery worker picks up job → Downloads dataset from MinIO → Processes data → Uploads results → Updates job status
4. **Result Retrieval**: Client queries job status → Retrieves result URI from MinIO

## Prerequisites

- **Docker** and **Docker Compose** (for infrastructure services)
- **Python 3.12+**
- **uv** (Python package manager) - [Installation Guide](https://github.com/astral-sh/uv)

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd async-processing-maryia
```

### 2. Install Dependencies with uv

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync
```

This will create a virtual environment and install all dependencies defined in `pyproject.toml`.

### 3. Environment Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your configuration values. See [Environment Variables](#environment-variables) section for details.

### 4. Start Infrastructure Services with Docker Compose

Start PostgreSQL, Redis, and MinIO:

```bash
docker compose up -d
```

This will start:
- **PostgreSQL** on port `5432`
- **Redis** on port `6379`
- **MinIO** on ports `9000` (API) and `9001` (Web UI)

Verify services are running:

```bash
docker compose ps
```

### 5. Run Database Migrations

Activate the virtual environment and run Alembic migrations:

```bash
# Activate the virtual environment (created by uv)
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Run migrations
alembic upgrade head
```

This will create all necessary database tables and apply any pending migrations.

### 6. Initialize MinIO Buckets

Access MinIO Console at `http://localhost:9001` and create the following buckets:
- `datasets` (for dataset storage)
- `job-results` (for job result storage)

Or use the MinIO CLI:

```bash
# Install mc (MinIO Client) if needed
# macOS: brew install minio/stable/mc
# Linux: wget https://dl.min.io/client/mc/release/linux-amd64/mc

mc alias set local http://localhost:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}
mc mb local/datasets
mc mb local/job-results
```

### 7. Start the Application

#### Start FastAPI Server

```bash
# Make sure you're in the virtual environment
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

#### Start Celery Worker

In a separate terminal:

```bash
# Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux

# Start Celery worker
celery -A workers.celery_app worker --loglevel=info
```

For development with auto-reload:

```bash
celery -A workers.celery_app worker --loglevel=info --reload
```

## Running the Application

### Quick Start (All Services)

1. **Start infrastructure**:
   ```bash
   docker compose up -d
   ```

2. **Run migrations**:
   ```bash
   source .venv/bin/activate
   alembic upgrade head
   ```

3. **Start FastAPI** (Terminal 1):
   ```bash
   source .venv/bin/activate
   uvicorn main:app --reload
   ```

4. **Start Celery Worker** (Terminal 2):
   ```bash
   source .venv/bin/activate
   celery -A workers.celery_app worker --loglevel=info
   ```

### Database Migrations

#### Create a New Migration

After modifying database models:

```bash
# Generate migration from model changes
alembic revision --autogenerate -m "description of changes"

# Review the generated migration file in alembic/versions/
# Then apply it
alembic upgrade head
```

#### Apply Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Apply migrations up to a specific revision
alembic upgrade <revision_id>

# Rollback one migration
alembic downgrade -1

# Rollback to a specific revision
alembic downgrade <revision_id>
```

#### Check Migration Status

```bash
# Show current database revision
alembic current

# Show migration history
alembic history

# Show pending migrations
alembic heads
```

### Celery Worker

#### Basic Worker

```bash
celery -A workers.celery_app worker --loglevel=info
```

#### Worker with Concurrency

```bash
# Run with 4 worker processes
celery -A workers.celery_app worker --loglevel=info --concurrency=4
```

#### Worker with Auto-reload (Development)

```bash
celery -A workers.celery_app worker --loglevel=info --reload
```

#### Monitor Celery Tasks

```bash
# Start Flower (Celery monitoring tool)
# First install: uv add flower
celery -A workers.celery_app flower
```

Access Flower at `http://localhost:5555`

## Environment Variables

The application requires the following environment variables (see `.env.example`):

### Database Configuration
- `POSTGRES_HOST`: PostgreSQL host (default: `localhost`)
- `POSTGRES_PORT`: PostgreSQL port (default: `5432`)
- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password

### MinIO/S3 Configuration
- `MINIO_ROOT_USER`: MinIO root user
- `MINIO_ROOT_PASSWORD`: MinIO root password
- `S3_ENDPOINT_URL`: S3 endpoint URL (default: `http://localhost:9000`)
- `S3_REGION`: S3 region (default: `us-east-1`)
- `S3_DATASETS_BUCKET`: Bucket name for datasets (default: `datasets`)
- `S3_JOB_RESULTS_BUCKET`: Bucket name for job results (default: `job-results`)

### Celery Configuration
- `CELERY_BROKER_URL`: Redis broker URL (default: `redis://localhost:6379/0`)
- `CELERY_RESULT_BACKEND`: Redis result backend URL (default: `redis://localhost:6379/0`)

## API Endpoints

### Datasets
- `POST /datasets` - Create a new dataset
- `GET /datasets/{dataset_id}` - Get dataset details

### Jobs
- `POST /jobs` - Create a new processing job
- `GET /jobs/{job_id}` - Get job status and details
- `GET /jobs/{job_id}/result` - Get job result URI
- `POST /jobs/{job_id}/cancel` - Cancel a running job

See interactive API documentation at `http://localhost:8000/docs` for detailed request/response schemas.

## Project Structure

```
async-processing-maryia/
├── alembic/                 # Database migrations
│   ├── versions/            # Migration files
│   └── env.py              # Alembic environment configuration
├── api/                     # FastAPI application
│   ├── routes/             # API route handlers
│   └── app.py              # FastAPI app factory
├── db/                      # Database layer
│   ├── models/             # SQLAlchemy ORM models
│   ├── config.py           # Database configuration
│   └── session.py          # Database session management
├── job_runners/             # Job execution interfaces
├── ports/                   # Port interfaces (dependency inversion)
├── repositories/            # Data access layer
│   ├── interfaces/         # Repository interfaces
│   └── sqlalchemy/         # SQLAlchemy implementations
├── schemas/                 # Pydantic schemas for API
├── services/                # Business logic services
│   └── storage/            # Storage service implementations
├── use_cases/               # Application use cases
├── workers/                 # Celery workers
│   ├── celery_app.py       # Celery application
│   ├── jobs.py             # Job task definitions
│   └── processing/         # Data processing modules
├── docker-compose.yml       # Infrastructure services
├── alembic.ini             # Alembic configuration
├── pyproject.toml           # Project dependencies (uv)
└── main.py                 # Application entry point
```

## Development

### Running Tests

```bash
# Install test dependencies
uv add --dev pytest pytest-asyncio

# Run tests
pytest
```

### Code Formatting

```bash
# Install formatter
uv add --dev black ruff

# Format code
black .
ruff check --fix .
```

## Troubleshooting

### Database Connection Issues

- Ensure PostgreSQL is running: `docker compose ps`
- Check database credentials in `.env`
- Verify network connectivity: `docker compose logs postgres`

### Celery Worker Not Processing Jobs

- Verify Redis is running: `docker compose ps`
- Check Celery broker URL in `.env`
- Review worker logs for errors
- Ensure worker is connected: Check for "ready" message in logs

### MinIO Connection Issues

- Verify MinIO is running: `docker compose ps`
- Check MinIO credentials in `.env`
- Ensure buckets are created (see [Initialize MinIO Buckets](#6-initialize-minio-buckets))
- Access MinIO console at `http://localhost:9001`

### Migration Issues

- Ensure database is running before running migrations
- Check `alembic.ini` configuration
- Verify database URL in `.env` matches `alembic/env.py` expectations
- Review migration files in `alembic/versions/` for errors

## License

[Add your license here]
