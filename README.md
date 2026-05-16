# Ground Control Station (Flask)
A web-based Robot Management System that acts as a Ground Control Station for a remote autonomous unit. The application integrates with a robot REST API, visualises telemetry on a 2D dashboard, enforces role-based access control, logs mission activity, and handles intermittent connectivity gracefully.

## Features
- Real-time telemetry polling from a robot HTTP API
- 2D grid dashboard with battery and connection status
- Secure user registration and login
- RBAC with `viewer` and `commander` roles
- Mission logging and telemetry audit trail stored in SQLite
- Resilient retry logic for variable latency and dropouts
- Docker and docker-compose setup
- Unit and integration tests with pytest
- GitHub Actions CI workflow

## Architecture and Design Patterns
- **Factory Pattern:** `create_app()` initialises the Flask application and dependencies.
- **Singleton Pattern:** `RobotClient` maintains one reusable robot communication client instance.
- **Observer Pattern:** telemetry updates are published through `TelemetrySubject`, with `TelemetryAuditObserver` persisting snapshots for auditability.
- **Separation of Concerns:** routes, services, models, templates, and static assets are isolated into dedicated modules.

## Quick Start

### 1. Run with Docker Compose
```bash
docker compose up --build
```

Open the dashboard at `http://localhost:5000`.

### 2. Run locally without Docker
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python run.py
```

## Demo Accounts
Register two users manually from the UI:
- Viewer account for read-only monitoring
- Commander account for issuing movement commands

## Swap in the University Robot Container
The compose file currently includes a compatible `mock_robot_api` service so the repo runs immediately. When the official university container is released, replace the `robot-api` service in `docker-compose.yml` with the provided image/container and keep `ROBOT_API_URL=http://robot-api:8001` or adjust to the correct port.

## Test Suite
```bash
pytest -q
```

## Suggested GitHub Upload Structure
```text
.
âââ app/
âââ mock_robot_api/
âââ tests/
âââ .github/workflows/ci.yml
âââ docker-compose.yml
âââ Dockerfile
âââ README.md
âââ requirements.txt
âââ requirements-dev.txt
âââ run.py
```

## Security Notes
- Passwords are stored using Werkzeug password hashing.
- Viewer role cannot issue movement commands.
- Audit logs preserve command history for safety and accountability.
- Add HTTPS, CSRF protection, stronger secret management, and production-grade database settings before real deployment.
