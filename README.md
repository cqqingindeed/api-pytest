# API Pytest

This is a demo API test-automation project for a job hunting. It is
under construction, and additional features will be added over time.

> **Note:** The application under test is not included in this repository yet.
> Until it is available and running, the test suite cannot produce or verify
> actual API results.

## Planned additions

- Environment configuration (dev/staging) through config files and environment variables
- A test-data folder containing JSON and CSV fixtures
- Shared fixtures, a reusable API client, and helper utilities
- Reporting with pytest-html or Allure
- Code-coverage measurement and reporting with `pytest-cov` for this pure-Python project (planned for implementation with the Agent API)
- Failure diagnostics, including useful request, response, and log details
- Test isolation and reliable cleanup of test data
- A CI pipeline with GitHub Actions or Jenkins
- A scripts folder for running tests and project setup

## Project structure

- `tests/` — API test cases, organised by feature area
- `clients/` — HTTP client code used by tests
- `helpers/` — reusable test helpers
- `configs/` — runtime settings and environment defaults
- `docs/` — test-case documentation
- `results/` — generated test-report output

## Usage

### Prerequisites

Use Python and install the project dependencies. When it becomes available,
start the API under test before executing the suite.

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
export BASE_URL="http://localhost:3050"
```

### Configuration

The test suite reads these optional environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `BASE_URL` | `http://localhost:3050` | Base URL of the API under test |
| `DEFAULT_USER_EMAIL` | `student@example.com` | Email for authenticated tests |
| `DEFAULT_USER_PASSWORD` | `Password123!` | Password for authenticated tests |

For example:

```bash
export BASE_URL="https://staging.example.com"
export DEFAULT_USER_EMAIL="tester@example.com"
export DEFAULT_USER_PASSWORD="your-password"
```

### Run test cases

Run the complete suite:

```bash
pytest
```

Run all cases in an area, such as authentication or applications:

```bash
pytest tests/auth
pytest tests/applications
```

Run one test file, one individual test, or tests matching a name:

```bash
pytest tests/auth/test_verify_login.py
pytest tests/auth/test_verify_login.py::test_verify_user_can_login_with_valid_credentials
pytest -k "login"
```

Run cases by their registered pytest marker:

```bash
python -m pytest -m AUTH
python -m pytest -m APPS
python -m pytest -m "AUTH or PUBLIC"
```

## Test results

Test output is shown in the terminal. Generated HTML reports are stored in
`results/` when reporting is enabled.

## Contributing

Add tests to the relevant feature folder under `tests/`. Reuse existing client
and helper code where appropriate, register any new pytest markers in
`pytest.ini`, and keep the corresponding test-case documentation up to date.

## License

No license has been selected for this project yet.
