"""Fail-closed internal-service guard; NOT user-level authentication or food certification."""
import os
import secrets
from fastapi import Header, HTTPException

def production_mode():
    return os.getenv("APP_ENV", "development").strip().lower() == "production"

def validate_deployment_config(values=None):
    """Validate deployment config before starting the application."""
    conf = values if values is not None else os.environ
    mode=conf.get("APP_ENV","development").strip().lower()
    if mode not in ("development","test","production"):
        raise RuntimeError("APP_ENV must be development, test or production")
    if mode != "production":
        return
    problems=[]
    key=conf.get("API_KEY","")
    if len(key)<32 or key.lower() in {"changeme","example","sample","secret"}:
        problems.append("Production API_KEY must be at least 32 random characters")
    if conf.get("SEED_DEMO_DATA","false").lower()!="false":
        problems.append("Production SEED_DEMO_DATA must be false")
    if not conf.get("DATABASE_URL","").startswith(("postgresql://","postgresql+psycopg://")):
        problems.append("Production requires a PostgreSQL DATABASE_URL")
    origins=[o.strip() for o in conf.get("CORS_ORIGINS","").split(",") if o.strip()]
    if any(not o.startswith("https://") for o in origins):
        problems.append("Production CORS_ORIGINS must be empty or exclusively HTTPS origins")
    if conf.get("ENABLE_REAL_OPERATIONS","false").lower()=="true":
        problems.append("Real operations are intentionally unavailable in this demo build")
    if problems:
        raise RuntimeError("; ".join(problems))

def valid_service_key(presented):
    key=os.getenv("API_KEY","")
    return bool(key and presented and secrets.compare_digest(key,presented))

def require_write_key(x_api_key: str | None=Header(default=None)):
    # Even a valid service key cannot override missing production identity,
    # tenant isolation, independently verified partners and food safety workflows.
    if production_mode():
        raise HTTPException(status_code=403,detail="Production operations disabled until independently audited onboarding and access controls are implemented")
    key=os.getenv("API_KEY","")
    if key and not valid_service_key(x_api_key):
        raise HTTPException(status_code=401,detail="Missing or invalid API key")
