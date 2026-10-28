"""FoodBridge AI — demonstration API. Never used as a food safety certification tool."""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.database import Base,engine,SessionLocal
from .db import models  # noqa: F401
from .db.seed import seed_demo
from .routes import inventory,recipients,donations,analytics
@asynccontextmanager
async def lifespan(app:FastAPI):
    if os.getenv("APP_ENV","development")=="production" and not os.getenv("API_KEY"):
        raise RuntimeError("Production requires API_KEY")
    Base.metadata.create_all(bind=engine)
    if os.getenv("SEED_DEMO_DATA","true").lower()=="true":
        with SessionLocal() as db:
            seed_demo(db)
    yield
app=FastAPI(title="FoodBridge AI",version="1.0.0",description="Educational synthetic food-surplus prototype; human safety review mandatory.",lifespan=lifespan)
origins=[s.strip() for s in os.getenv("CORS_ORIGINS","http://localhost:5173,http://localhost:3000").split(",") if s.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=False,allow_methods=["GET","POST"],allow_headers=["Content-Type","X-API-Key"])
@app.get("/api/v1/health")
def health():
    return {"status":"ok","service":"FoodBridge AI","environment":os.getenv("APP_ENV","development")}
for router in (inventory.router,recipients.router,donations.router,analytics.router):
    app.include_router(router,prefix="/api/v1")
