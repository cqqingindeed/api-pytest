# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A pytest + requests test-automation suite for an external "job tracker" REST API (`/api/v1/...`). The application under test is **not** in this repo; tests only pass when it is running at `BASE_URL`. There is no build step and no linter configured.

## Commands

Always run from the repo root (imports like `from clients.api_client import APIClient` rely on the root `conftest.py` putting the root on `sys.path`).

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt     # pytest, requests, pytest-html

pytest                                          # whole suite
pytest tests/auth                               # one feature area
pytest tests/auth/test_verify_login.py::test_verify_user_can_login_with_valid_credentials
pytest -k "login"
python -m pytest -m AUTH                        # by area marker (AUTH, APPS, APPNEG, APIKEY, AUDIT, PUBLIC)
pytest --html=results/report.html               # HTML report (pytest-html)
pytest --collect-only -q tests/<path>           # check imports/markers without running
```

Config is via env vars read in `configs/settings.py`: `BASE_URL` (default `http://localhost:3050`), `DEFAULT_USER_EMAIL`, `DEFAULT_USER_PASSWORD`, `DATABASE_PATH` (SQLite file of the app under test; the default is an absolute path on the author's machine).

## Architecture

- **`clients/api_client.py` — `APIClient`** is the only HTTP layer. Constructing it with `authenticated=True` (the default) **logs in immediately** (`POST /api/v1/auth/login`) and stores a Bearer token. Methods `get/post/patch/delete` and `*_json` variants take an endpoint path (not a full URL) and an `expected_status_code`, and **assert the status code themselves** — negative tests pass the expected 4xx code rather than checking it afterwards. `delete` defaults to 204, `post` to 200 (resource creation passes 201 explicitly via helpers).
- **`clients/sql_client.py` — `SQLClient`** queries the app's SQLite DB directly (used e.g. for API-key storage and audit-log checks); requires `DATABASE_PATH` to exist locally.
- **`helpers/`** hold domain actions on top of the client: `application_helper.build_create_applicaiton_payload(**overrides)` (note the misspelling — it's the real name) returns a valid default payload that tests mutate; `create_application` / `get_application` / `delete_application`; `error_helper.verify_error_response` checks the API's `{"error": {"code", "message", "details"}}` envelope (validation errors are 422 / `VALIDATION_ERROR` with `details[].loc` and `.type`).
- **`conftest.py`** provides fixtures `api_client`, `unauthenticated_api_client`, and `create_application_fixture` (creates an application, yields it, deletes it after). It also adds a `--tcid` option that filters on a `tcid` marker — but tests currently use the area markers (`@pytest.mark.AUTH("001")`), so `--tcid` selects nothing today.
- **Markers ↔ docs:** each area marker's argument is a test-case number that maps to a row in `docs/*.csv` (e.g. `APPNEG-CREATE-001`). Those CSVs are the test-case specs (steps, expected result, `automation_status`, `source_test`); keep them in sync when automating a case. New markers must be registered in `pytest.ini`.

### Gotchas

- Several test modules create `APIClient()` at module level (e.g. `tests/auth/test_verify_login.py`, `tests/applications/test_verify_update_application_field.py`). With the API down, **collecting the whole suite fails** with connection errors — not a code bug. Prefer the `api_client` fixture in new tests.
- Tests that create data must clean it up (fixture with `yield`, or `try/finally`); in `finally`, guard against IDs that were never assigned when creation fails.

## Claude Code setup in this repo

- **Stop hook** (`.claude/hooks/verify-changes.sh`, wired in `.claude/settings.json`): on every stop, compiles changed `.py` files, collects changed tests, runs them if the API is reachable, and blocks on failure; prints a per-file change summary. Set `SKIP_VERIFY_HOOK=1` for headless jobs that change no code.
- **Planning flow for new projects/features:** `research-to-slides` skill → `docs/todo/<name>_blueprint.txt`; then the `evident-research` agent verifies the blueprint's references and writes `docs/design/<name>_design.txt`; implement only after the user approves the design. `docs/todo/`, `docs/design/` and `docs/status/` are git-ignored by design.
- **`code-reviewer` agent** reviews changes against the conventions above (read-only).
- **Weekly status:** `.claude/scheduled/weekly-status.sh` runs `claude -p` to write `docs/status/<MM-DD-YYYY>.docx` (via `build_status_docx.py` and its own `.venv`). Not scheduled; run manually.
- Don't commit unless the user asks.
