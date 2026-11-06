# ARAD Identity & RBAC Demo

Demonstration of Okta OIDC Authentication and Role-Based Access Control (RBAC) with FastAPI, Authlib, and Starlette SessionMiddleware.

## Project Structure

```text
arad-identity-demo/
│
├── app.py                     # Main FastAPI app with Okta OIDC & RBAC dependencies
├── requirements.txt           # Python dependencies
├── .env                       # Local environment variables & secrets (git-ignored)
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore rules
├── pytest.ini                 # Pytest configuration
├── README.md                  # Project documentation
│
├── tests/
│   └── test_app.py            # Automated tests for auth, RBAC, and dev personas
│
└── .github/
    └── workflows/
        └── ci.yml             # GitHub Actions CI workflow
```

## Features

- **Okta OIDC Integration**: Authorization Code flow via Authlib with automatic discovery metadata.
- **BFF Security Model**: Tokens stay server-side; identity claims (`sub`, `name`, `email`, `roles`) are signed in an HTTP session cookie.
- **Role-Based Access Control (RBAC)**: `require_role(*roles)` dependency protecting endpoints:
  - `/api/developer/apps` &mdash; Requires `developer` or `platform_admin`
  - `/api/manager/approvals` &mdash; Requires `manager` or `platform_admin`
  - `/api/admin/audit` &mdash; Requires `platform_admin` or `leadership`
- **Configurable Group Mapping**: Reads claims from `OKTA_GROUPS_CLAIM` (default `groups`) and maps to ARAD roles.
- **Local Dev Persona Switcher**: When `AUTH_MODE=dev` and `ENV=local`, switch between Alice (developer), Bob (manager), Charlie (data owner), Dave (admin), and Eve (leadership) without live Okta login.
- **Production Guard**: App refuses to start if `AUTH_MODE=dev` is attempted in staging or production (`ENV!=local`).

## Setup & Running

1. **Activate virtual environment**:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

2. **Configure `.env`**:
   ```env
   OKTA_ISSUER=https://<your-okta-domain>/oauth2/default
   OKTA_CLIENT_ID=<your-client-id>
   OKTA_CLIENT_SECRET=<your-client-secret>
   SESSION_SECRET=<random-32-byte-secret>
   OKTA_GROUPS_CLAIM=groups
   ENV=local
   AUTH_MODE=dev
   ```

3. **Start the application**:
   ```powershell
   uvicorn app:app --reload
   ```
   Visit [http://127.0.0.1:8000](http://127.0.0.1:8000).

4. **Run the test suite**:
   ```powershell
   pytest
   ```
