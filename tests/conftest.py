"""Isolated integration tests; never mutate the user's persistent demo DB."""
import os
os.environ["SEED_DEMO_DATA"]="false"
os.environ["APP_ENV"]="development"
os.environ["API_KEY"]=""
os.environ["DEMO_ADMIN_KEY"]="local-demo-only-administrator-key-123456"
os.environ["DATABASE_URL"]="sqlite://"
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from backend.app.db.database import Base,get_db
from backend.app.db import models
from backend.app.main import app
@pytest.fixture()
def client():
    eng=create_engine("sqlite://",connect_args={"check_same_thread":False},poolclass=StaticPool)
    Base.metadata.create_all(bind=eng)
    Session=sessionmaker(bind=eng,expire_on_commit=False)
    def override():
        with Session() as s:yield s
    app.dependency_overrides[get_db]=override
    with TestClient(app) as c:yield c
    app.dependency_overrides.clear()
    eng.dispose()
