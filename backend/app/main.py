"""FoodBridge AI demo API; production mode is a closed, read-only staging shell."""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from .db.database import Base,engine,SessionLocal
from .db import models  # noqa: F401
from .db.seed import seed_demo
from .routes import inventory,recipients,donations,analytics,audit
from .security import production_mode,validate_deployment_config,valid_service_key

@asynccontextmanager
async def lifespan(app:FastAPI):
    validate_deployment_config()
    if not production_mode():
        Base.metadata.create_all(bind=engine)
        if os.getenv("SEED_DEMO_DATA","true").lower()=="true":
            with SessionLocal() as db:
                seed_demo(db)
    # In production, initialize schema explicitly with an audited migration plan.
    yield

app=FastAPI(
    title="FoodBridge AI",version="1.1.0",
    description="Synthetic educational demo; never automatic food safety certification.",
    docs_url=None if production_mode() else "/docs",
    redoc_url=None if production_mode() else "/redoc",
    openapi_url=None if production_mode() else "/openapi.json",
    lifespan=lifespan
)
origins=[s.strip() for s in os.getenv("CORS_ORIGINS","http://localhost:5173,http://localhost:3000").split(",") if s.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=False,allow_methods=["GET","POST"],allow_headers=["Content-Type","X-API-Key"])

@app.middleware("http")
async def security_boundary(request:Request,call_next):
    # Operational endpoints are not exposed without the service secret in
    # production. Never put this key in browser JavaScript.
    if production_mode() and request.url.path.startswith("/api/v1/") and request.url.path not in ("/api/v1/health","/api/v1/ready"):
        if not valid_service_key(request.headers.get("x-api-key")):
            return JSONResponse(status_code=401,content={"detail":"Authentication required"},headers={"Cache-Control":"no-store"})
    response=await call_next(request)
    response.headers["X-Content-Type-Options"]="nosniff"
    response.headers["X-Frame-Options"]="DENY"
    response.headers["Referrer-Policy"]="no-referrer"
    response.headers["Cache-Control"]="no-store"
    return response

@app.get("/api/v1/health")
def health():
    return {"status":"ok","service":"FoodBridge AI","mode":"internal-staging" if production_mode() else "demo"}

@app.get("/api/v1/ready")
def ready():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status":"ready","database":"connected"}
    except Exception:
        return JSONResponse(status_code=503,content={"status":"not_ready"})

for router in (inventory.router,recipients.router,donations.router,analytics.router,audit.router):
    app.include_router(router,prefix="/api/v1")
