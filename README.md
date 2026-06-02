# StrangerCalc

A full-stack web calculator built with **Flask** and **PostgreSQL**. The browser UI sends JSON to a REST API; each operation can be persisted per session so you can audit or extend with history features later.

## Demo video

Watch the demo here: [Canva demo video](https://canva.link/t759kqiqw0rijcu)

## About this project

This project was built to practice backend development with Python and Flask, focusing on REST API design, database integration, and session management. It demonstrates my ability to structure a full-stack application, connect a frontend to a backend API, and persist data using PostgreSQL.

## Features

- **Web UI** — calculator with keyboard support (`templates/`, `static/`)
- **Session-scoped state** — Flask sessions map each visitor to a `Calculator` instance
- **REST API** — JSON endpoints for arithmetic, reset, and history
- **PostgreSQL** — calculations and session snapshots stored via `psycopg2`
- **Configurable** — database and secrets via environment variables (see [Configuration](#configuration))
- **UI tests** — end-to-end browser tests with Playwright (see [UI testing](#ui-testing))

## Tech stack

| Layer        | Technology                          |
|-------------|--------------------------------------|
| Backend     | Python 3, Flask 3                    |
| Database    | PostgreSQL 15 (local or Docker)      |
| Frontend    | HTML, CSS, vanilla JavaScript        |
| UI testing  | Playwright (`@playwright/test`)      |
| Packaging   | `venv`, optional Docker / Compose    |

## Architecture (high level)

1. The **frontend** calls `POST /api/calculate` with operands and an operator.
2. **Flask** (`app.py`) resolves the current session, obtains a `Calculator`, and runs the operation.
3. The **calculator** uses the **database** layer to `INSERT` into `calculations` and upsert `sessions`.
4. The API returns JSON; the UI updates the display.

## Prerequisites

- Python **3.11+** recommended (3.13 works if dependencies install cleanly)
- **PostgreSQL** running locally, or **Docker Desktop** for the Compose setup

## Local setup

### 1. Clone and virtual environment

```bash
git clone <your-repo-url>
cd strangercalc
python -m venv venv
```

**Windows (PowerShell)**

```powershell
.\venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

**macOS / Linux**

```bash
source venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. PostgreSQL

Create a database and user (names can match your `.env`). Example:

```sql
CREATE DATABASE strangercalc;
CREATE USER postgres WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE strangercalc TO postgres;
```

On first request, the app creates `calculations` and `sessions` tables if they do not exist.

### 3. Environment variables

Copy `backend/.env.example` to **`.env` in the project root** (same folder as `app.py`) so `load_dotenv()` picks it up when you run from the root, **or** set variables in your shell.

| Variable       | Description                    | Example        |
|----------------|--------------------------------|----------------|
| `DB_HOST`      | PostgreSQL host                | `localhost`    |
| `DB_NAME`      | Database name                  | `strangercalc` |
| `DB_USER`      | Database user                  | `postgres`     |
| `DB_PASSWORD`  | Database password (required)   | —              |
| `DB_PORT`      | Port                           | `5432`         |
| `SECRET_KEY`   | Flask session signing (required) | long random string |
| `DEBUG`        | Flask debug flag               | `False`        |

`DB_PASSWORD` and `SECRET_KEY` must be set; there are no default secrets in code.

### 4. Run the application

From the **repository root** (where `app.py` lives):

```bash
python app.py
```

Open **http://127.0.0.1:8000** in a browser.

## UI testing

End-to-end UI tests use [Playwright](https://playwright.dev/) to drive the calculator in a real browser. They match three manual test cases (addition, invalid input validation, and UI layout).

### What is covered

| Test case | Playwright test | How it maps to the UI |
|-----------|-----------------|------------------------|
| Successful calculation of two numbers | `successful addition of two numbers` | Enters `2 + 3` on the keypad and clicks **=** (the calculate action). Expects display `5`. |
| Empty / invalid input validation | `shows error when calculation input is invalid` | The app uses a single display instead of two form fields. Invalid input is exercised with `5 ÷ 0`; the display shows `Error!` and the UI stays usable. |
| Essential UI elements on load | `renders essential UI elements on load` | Checks heading, display, **=** button, layout container, and that `style.css` is loaded. |

Tests live in `tests/calculator.spec.js`. Playwright starts the Flask app automatically via `playwright.config.js` (using `venv` Python on port `8000`).

### Prerequisites

1. Complete [Local setup](#local-setup) (Python venv, PostgreSQL, root `.env` with `DB_PASSWORD` and `SECRET_KEY`).
2. Install Node dependencies and Playwright browsers:

```bash
npm install
npx playwright install
```

### Run tests

From the repository root:

```bash
npm run test:ui
```

Other useful commands:

```bash
npm run test:ui:headed    # run with a visible browser
npm run test:ui:report      # open the HTML report after a run
```

If the app is already running on port `8000`, Playwright reuses it locally (`reuseExistingServer`). In CI, the config starts a fresh server for each run.

### Notes

- UI tests call the real `/api/calculate` endpoint, so PostgreSQL must be reachable with the credentials in `.env`.
- GitHub Actions runs `npx playwright test` on push/PR; ensure CI has PostgreSQL and the same environment variables if you want those jobs to pass.

## Docker (optional)

`docker-compose.yml` is **gitignored** so database passwords are never pushed to GitHub. Use the tracked template and a root `.env` file for secrets.

1. Copy the template (once per machine / clone):

   ```bash
   cp docker-compose.example.yml docker-compose.yml
   ```

2. Create or extend a **`.env` file in the project root** (also gitignored). You can start from `docker.env.example`:

   ```bash
   cp docker.env.example .env
   ```

   Set **`POSTGRES_PASSWORD`** and **`DB_PASSWORD`** to the **same** value so the app container can connect to Postgres.

3. With Docker Desktop installed:

   ```bash
   docker compose up --build
   ```

- **App:** http://localhost:8000  
- **Postgres:** port `5432` (edit `docker-compose.yml` locally if it conflicts with a local instance)

Never commit `.env` or a `docker-compose.yml` that contains literal passwords.

## API overview

All JSON APIs return `{ "status": "success" | "error", ... }` unless noted.

| Method | Path | Body / query | Description |
|--------|------|--------------|-------------|
| `POST` | `/api/calculate` | `{ "first_operand", "second_operand", "operator" }` | Binary operation (`+`, `-`, `*`, `/`) — used by the main UI |
| `POST` | `/api/add` | `{ "number" }` | Add to running total |
| `POST` | `/api/subtract` | `{ "number" }` | Subtract from running total |
| `POST` | `/api/multiply` | `{ "number" }` | Multiply running total |
| `POST` | `/api/divide` | `{ "number" }` | Divide running total |
| `POST` | `/api/reset` | — | Reset running total |
| `GET`  | `/api/result` | — | Current running total |
| `GET`  | `/api/history` | `?limit=10` | Recent calculations for this calculator session |
| `GET`  | `/api/session` | — | Session / calculator identifiers (debug) |

## Project structure

```
strangercalc/
├── app.py                       # Flask app and routes
├── Dockerfile                   # Container image (root context)
├── docker-compose.example.yml   # Compose template (no secrets; copy to docker-compose.yml)
├── docker.env.example           # Sample vars for Docker Compose `.env`
├── init.sql                     # Optional DB init scripts (Compose)
├── playwright.config.js         # Playwright config (base URL, webServer)
├── tests/
│   └── calculator.spec.js       # UI end-to-end tests
├── package.json                 # Node deps (Playwright)
├── static/                # CSS, assets
├── templates/             # Jinja2 HTML
├── backend/
│   ├── calculator.py      # Domain logic + persistence hooks
│   ├── database.py        # PostgreSQL access
│   ├── config.py          # Environment configuration
│   ├── requirements.txt   # Python dependencies
│   └── .env.example       # Sample environment file
└── venv/                  # Local virtualenv (not committed)
```

## Security note

Do not commit real `.env` files, `docker-compose.yml` with embedded passwords, or production secrets. Use strong `SECRET_KEY` and database passwords in any shared or hosted environment. If a password was ever committed, rotate it and rely on `.env` plus the example Compose file going forward.

## Author

**Kelli Kirk**

- **School / GitHub:** [kelli.kirk@voco.ee](mailto:kelli.kirk@voco.ee)  
- **Job applications:** [kelkirk93@gmail.com](mailto:kelkirk93@gmail.com)
