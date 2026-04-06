# Agent Flow 🚀

Production-ready AI workflow builder with FastAPI, Temporal, and React Flow.

## Tech Stack
- **Backend**: FastAPI, Temporal, MySQL, Redis, LiteLLM
- **Frontend**: React, TypeScript, React Flow, Tailwind CSS
- **Infrastructure**: Docker Compose, UV (Python package manager)

## Prerequisites
- **Docker & Docker Compose**
- **Node.js** (v18+) & **NPM**
- **UV** (modern Python package manager)
- **Temporal CLI** (for local development outside Docker)

## Getting Started

### 1. Setup Environment Variables
Clone the `.env.example` file and fill in your API keys:

```bash
cp .env.example .env
```

### 2. Run Backend with Docker Compose
From the root directory:

```bash
docker compose up --build
```

### 3. Setup Frontend
Navigate to the `frontend` directory and install dependencies:

```bash
cd frontend
npm install
npm run dev
```

## Local Development URLs

| Service | URL |
| :--- | :--- |
| **Frontend** | [http://localhost:5173](http://localhost:5173) |
| **FastAPI Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) |
| **Temporal Web UI** | [http://localhost:8233](http://localhost:8233) |
| **Mailpit (Local Email)** | [http://localhost:8025](http://localhost:8025) |

## Database Migrations
We use Alembic for async database migrations. To initialize or update the database:

```bash
# Generate a new migration
docker compose exec fastapi_app alembic revision --autogenerate -m "initial_schema"

# Apply migrations
docker compose exec fastapi_app alembic upgrade head
```

## Temporal Server Setup
We recommend running a local Temporal development server on your host machine for better observability:

### Install Temporal CLI
Follow the guide at [Temporal Documentation](https://learn.temporal.io/tutorials/python/background-check/project-setup/#install-cli).

### Start Temporal Server
```bash
temporal server start-dev
```

## Code Quality
We use `ruff` for linting and formatting.

```bash
# Lint code
uv run ruff check --fix

# Format code
uv run ruff format
```

***

Copyright (C) 2026 - All Rights Reserved
