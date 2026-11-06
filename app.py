import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth

load_dotenv()

app = FastAPI(title="ARAD Identity Demo")

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "super-secret-key"),
    max_age=3600,
)

# Okta OIDC Configuration
okta_issuer = os.getenv("OKTA_ISSUER", "").rstrip("/")
metadata_url = f"{okta_issuer}/.well-known/openid-configuration" if okta_issuer else None

oauth = OAuth()
oauth.register(
    name="okta",
    client_id=os.getenv("OKTA_CLIENT_ID"),
    client_secret=os.getenv("OKTA_CLIENT_SECRET"),
    server_metadata_url=metadata_url,
    client_kwargs={"scope": "openid profile email"},
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = request.session.get("user")
    
    css = """
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #f5f7fb 0%, #e8edf5 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
            color: #1e293b;
        }
        .card {
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
            width: 100%;
            max-width: 480px;
            padding: 36px;
            border: 1px solid #e2e8f0;
        }
        .header {
            text-align: center;
            margin-bottom: 28px;
        }
        .title {
            font-size: 24px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 8px;
        }
        .subtitle {
            font-size: 14px;
            color: #64748b;
        }
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            background: #ecfdf5;
            color: #059669;
            border: 1px solid #a7f3d0;
            border-radius: 9999px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 20px;
        }
        .badge-dot {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
        }
        .info-group {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 24px;
        }
        .info-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            font-size: 14px;
            border-bottom: 1px solid #edf2f7;
        }
        .info-row:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }
        .info-label {
            color: #64748b;
            font-weight: 500;
        }
        .info-val {
            font-weight: 600;
            color: #0f172a;
            font-family: monospace;
            font-size: 13px;
        }
        .btn {
            display: block;
            width: 100%;
            text-align: center;
            padding: 12px 20px;
            border-radius: 10px;
            font-size: 15px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s ease;
            cursor: pointer;
        }
        .btn-primary {
            background: #2563eb;
            color: #ffffff;
            border: none;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        }
        .btn-primary:hover {
            background: #1d4ed8;
            box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
        }
        .btn-secondary {
            background: #f1f5f9;
            color: #334155;
            margin-bottom: 12px;
        }
        .btn-secondary:hover {
            background: #e2e8f0;
        }
        .btn-logout {
            background: transparent;
            color: #dc2626;
            border: 1px solid #fecaca;
        }
        .btn-logout:hover {
            background: #fef2f2;
        }
    </style>
    """

    if user:
        name = user.get("name") or "User"
        email = user.get("email") or "Not provided"
        sub = user.get("sub") or "N/A"

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>ARAD Identity Demo</title>
            {css}
        </head>
        <body>
            <div class="card">
                <div class="header">
                    <span class="badge"><span class="badge-dot"></span> Identity Verified</span>
                    <h1 class="title">ARAD Identity Demo</h1>
                    <p class="subtitle">Authenticated via Okta OIDC</p>
                </div>

                <div class="info-group">
                    <div class="info-row">
                        <span class="info-label">Name</span>
                        <span class="info-val">{name}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Email</span>
                        <span class="info-val">{email}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Subject ID</span>
                        <span class="info-val">{sub}</span>
                    </div>
                </div>

                <a href="/me" class="btn btn-secondary">View Profile JSON</a>
                <a href="/logout" class="btn btn-logout">Logout</a>
            </div>
        </body>
        </html>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>ARAD Identity Demo</title>
        {css}
    </head>
    <body>
        <div class="card">
            <div class="header">
                <h1 class="title">ARAD Identity Demo</h1>
                <p class="subtitle">Demonstration of Okta authentication using OIDC.</p>
            </div>
            <a href="/login" class="btn btn-primary">Login with Okta</a>
        </div>
    </body>
    </html>
    """


@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.okta.authorize_redirect(request, redirect_uri)


@app.get("/auth/callback", name="auth_callback")
async def auth_callback(request: Request):
    token = await oauth.okta.authorize_access_token(request)
    userinfo = token.get("userinfo")
    if not userinfo:
        return JSONResponse(
            {"error": "User information was not returned"},
            status_code=400,
        )
    request.session["user"] = {
        "sub": userinfo.get("sub"),
        "name": userinfo.get("name"),
        "email": userinfo.get("email"),
    }
    return RedirectResponse("/", status_code=303)


@app.get("/me")
async def profile(request: Request):
    user = request.session.get("user")
    if not user:
        return JSONResponse(
            {"error": "Authentication required"},
            status_code=401,
        )
    return user


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)
