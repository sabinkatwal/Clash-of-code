# Clash of code

A small competitive coding platform backend and admin utilities project.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Installation & Setup](#installation--setup)
- [Database & Migrations](#database--migrations)
- [Running the App](#running-the-app)
- [API Routes](#api-routes)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

`Clash of code` is a lightweight backend for a coding battle / challenge platform. It includes API routes, a database layer (SQLAlchemy models), migration setup (Alembic), and a small admin GUI script for local management.

This repository contains a backend service and example app code to run and develop the project locally.

## Features

- User model and authentication scaffolding
- Match, Submission, and Rating models to support coding matches
- Alembic migrations for schema evolution
- Simple admin GUI utility for local tasks
- Websocket support (folder placeholder) for real-time features

## Tech Stack

- Python 3.10+ (recommended)
- FastAPI (recommended for `app/main.py` style apps)
- SQLAlchemy for ORM
- Alembic for migrations
- Optional websocket libraries for real-time features

## Repository Structure

Top-level important files and folders:

- `alembic.ini` — Alembic configuration
- `backend/` — Backend utilities and admin GUI
  - `admin_gui.py` — Small admin GUI / runner script
- `app/` — FastAPI application and API routes
  - `main.py` — Application entrypoint
  - `api/routes/` — API route modules (e.g., `auth.py`, `users.py`)
- `app/core/` — Core configuration and security helpers
- `app/database/` — DB setup, session, and models
  - `models/` — SQLAlchemy models: `user.py`, `match.py`, `rating.py`, `submission.py`
- `app/schemas/` — Pydantic schemas
- `app/services/` — Business logic (service layer)
- `app/websocket/` — Websocket related code (placeholder)
- `requirements.txt` — Python dependencies for the backend

## Requirements

Ensure you have Python 3.10 or higher installed. It's recommended to use a virtual environment.

Install dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

If you don't have `requirements.txt` updated, add the typical packages used by this project, for example:

```text
fastapi
uvicorn[standard]
sqlalchemy
alembic
pydantic
python-dotenv
websockets
```

## Installation & Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies with `pip install -r requirements.txt`.
4. Configure environment variables (database URL, secret keys). Use a `.env` file or your environment.

Typical environment variables used by the project (examples):

```
DATABASE_URL=sqlite:///./dev.db
SECRET_KEY=change_me_to_a_secure_value
```

Place them in a `.env` file (if using `python-dotenv`) or export them in your shell.

## Database & Migrations

The project uses Alembic for database migrations. To initialize and run migrations:

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

The `alembic/versions/` folder contains tracked migration scripts. If you use a different database (Postgres/MySQL), update `alembic.ini` and your `DATABASE_URL` accordingly.

## Running the App

### FastAPI Server

Run the FastAPI app using Uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Admin GUI

The admin panel provides a user-friendly interface to manage database tables. Run it from the `backend` directory:

```bash
python admin_gui.py
```

**Admin GUI Features:**

- **View Records**: Browse all records in each table with sortable columns
- **Add Records**: Create new entries via an intuitive form dialog
- **Edit Records**: Select and modify existing records
- **Delete Records**: Remove records with confirmation dialog
- **Refresh Data**: Reload table data from the database
- **Multiple Tables**: Manage Users, Matches, Submissions, and Ratings

**Tabs:**

- **👥 Users** — Manage user accounts (username, email, password)
- **🎮 Matches** — Create and manage coding matches
- **📝 Submissions** — View code submissions for matches
- **⭐ Ratings** — Track user ratings for matches

The admin GUI automatically connects to your configured database and displays real-time data.

## API Routes

Routes are located in `app/api/routes/`.

- `auth.py` — Authentication endpoints (login, token)
- `users.py` — User CRUD endpoints

Refer to the route modules for exact path names and payload schemas.

## Development

- Follow the repository structure when adding features: add models in `app/database/models`, schemas in `app/schemas`, and routes under `app/api/routes`.
- Use the service layer (`app/services`) for business logic to keep routes thin.
- Write migration scripts via Alembic when altering models.

Local development checklist:

1. Activate your venv.
2. Install dependencies.
3. Set environment variables.
4. Start the app via Uvicorn or the `admin_gui.py` helper.

## Testing

Add tests under a `tests/` folder. Use `pytest` for running tests. Example:

```bash
pip install pytest
pytest -q
```

When writing tests that use the database, prefer a temporary SQLite DB or transaction-based fixtures to keep tests isolated.

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/my-feature`.
3. Add your feature, tests, and documentation.
4. Open a pull request describing your changes.

Please keep changes focused and provide tests where applicable.

## Troubleshooting

- If migrations fail, confirm `DATABASE_URL` is set and reachable.
- If dependency errors occur, recreate the virtual environment and reinstall.
- For import errors, ensure `PYTHONPATH` includes the project root or run commands from the repository root.

 
