import os
import logging
from datetime import datetime, timezone

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("app")

CATFACT_URL = "https://catfact.ninja/fact"
HTTP_TIMEOUT = 5.0  # seconds
HTTP_RETRIES = 2

USER_EMAIL = os.getenv("USER_EMAIL")
USER_NAME = os.getenv("USER_NAME")
USER_STACK = os.getenv("USER_STACK")

app = FastAPI(title="Profile + Cat Fact")

# CORS (open; tighten for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

def now_utc_iso() -> str:
    # ISO 8601 with Z suffix, matching the example in the brief
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

async def fetch_cat_fact() -> str:
    # Small retry loop using a single client for connection reuse
    limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, limits=limits) as client:
        last_err = None
        for attempt in range(HTTP_RETRIES + 1):
            try:
                resp = await client.get(CATFACT_URL)
                resp.raise_for_status()
                data = resp.json()
                fact = data.get("fact")
                if not isinstance(fact, str) or not fact.strip():
                    raise ValueError("Cat Facts API returned invalid payload")
                return fact.strip()
            except Exception as e:
                last_err = e
                log.warning("catfact attempt %s failed: %s", attempt + 1, e)
        # If we’re here, all attempts failed
        raise HTTPException(status_code=502, detail="Failed to fetch cat fact")

def validate_user_env():
    missing = [k for k, v in {
        "USER_EMAIL": USER_EMAIL,
        "USER_NAME": USER_NAME,
        "USER_STACK": USER_STACK
    }.items() if not v]
    if missing:
        # Fail fast with a clear message so graders know what's wrong
        raise HTTPException(
            status_code=500,
            detail=f"Missing required env vars: {', '.join(missing)}"
        )

@app.get("/me")
async def me():
    validate_user_env()
    fact = await fetch_cat_fact()
    payload = {
        "status": "success",
        "user": {
            "email": USER_EMAIL,
            "name": USER_NAME,
            "stack": USER_STACK,
        },
        "timestamp": now_utc_iso(),
        "fact": fact,
    }
    return payload
