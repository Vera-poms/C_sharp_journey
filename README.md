# C# Journey

A learn-C# course app: React + Vite frontend, FastAPI backend, PostgreSQL (via SQLAlchemy) for course content and progress. Runs under Podman.

## Run

```
podman compose up --build
```

Open http://localhost:8080. Nginx serves the SPA and proxies `/api` to the FastAPI service; the database is seeded on first start and persists in the `pgdata` volume.

Reset all progress and content: `podman compose down -v`.

## Layout

- `backend/app/models.py` — modules, lessons, lesson_progress, lab_submissions
- `backend/app/seed_content.py` — module/lesson outline; aggregates the per-module lesson files `backend/app/content_m1.py` … `content_m8.py` (built with the helpers in `lesson_kit.py`). Content is re-synced into the database on every start, so edits show up after `podman compose up --build` without resetting progress.
- `backend/verify_content.py` — run `python verify_content.py [module numbers]` from `backend/` (needs the .NET SDK) to compile and run every code-along and lab solution and check each lab's expected output.
- `runner/` — .NET 10 SDK container with a small ASP.NET service. Each Run/Submit compiles and executes the learner's code in a throwaway project copy (build 60s, run 10s, output capped). It runs as an unprivileged user on an internal network with no internet access.
- `backend/app/runner.py` — calls the runner. A lab passes when the program's real output matches the lesson's `expected_output`.

Security: the app listens on `127.0.0.1:8080` only (edit the `ports` entry in `compose.yaml` to expose it on your LAN). The database is on its own internal network that only the API can reach; the runner is on a separate internal network with no internet and no route to the database, runs with a read-only filesystem and no capabilities, and nginx rate-limits the code-execution endpoints. Set `POSTGRES_PASSWORD` in a `.env` file to change the database password (on an existing volume, run `podman compose down -v` first).

Note: the runner has no memory/CPU/pids limits because the default Podman VM lacks those cgroup controllers. Add `mem_limit`/`cpus`/`pids_limit` to `compose.yaml` if your setup supports them.
- `frontend/src` — dashboard and lesson pages

## Develop without containers

```
# API (needs a Postgres reachable via DATABASE_URL)
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload
# Web
cd frontend && npm install && npm run dev
```
