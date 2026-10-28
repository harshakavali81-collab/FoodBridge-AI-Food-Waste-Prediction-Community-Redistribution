import pytest
from fastapi import HTTPException
from backend.app.security import validate_deployment_config,require_write_key

def production_config(**kwargs):
    config={
        "APP_ENV":"production",
        "API_KEY":"a"*40,
        "SEED_DEMO_DATA":"false",
        "DATABASE_URL":"postgresql+psycopg://user:password@db:5432/foodbridge",
        "CORS_ORIGINS":"https://example.org",
    }
    config.update(kwargs)
    return config

def test_dev_without_key_is_allowed():
    validate_deployment_config({"APP_ENV":"development"})

@pytest.mark.parametrize("changes",[
    {"API_KEY":""},
    {"API_KEY":"short"},
    {"SEED_DEMO_DATA":"true"},
    {"DATABASE_URL":"sqlite:///tmp/data.db"},
    {"CORS_ORIGINS":"http://example.org"},
    {"ENABLE_REAL_OPERATIONS":"true"},
])
def test_production_rejects_unsafe_settings(changes):
    with pytest.raises(RuntimeError):
        validate_deployment_config(production_config(**changes))

def test_production_accepts_read_only_staging_shape():
    validate_deployment_config(production_config())

def test_production_blocks_mutations_even_with_key(monkeypatch):
    monkeypatch.setenv("APP_ENV","production")
    monkeypatch.setenv("API_KEY","a"*40)
    with pytest.raises(HTTPException) as exc:
        require_write_key("a"*40)
    assert exc.value.status_code==403

def test_dev_optional_key(monkeypatch):
    monkeypatch.setenv("APP_ENV","development")
    monkeypatch.delenv("API_KEY",raising=False)
    require_write_key(None)
    monkeypatch.setenv("API_KEY","a"*40)
    with pytest.raises(HTTPException) as exc:
        require_write_key("wrong")
    assert exc.value.status_code==401

def test_response_safety_headers(client):
    response=client.get("/api/v1/health")
    assert response.headers["x-content-type-options"]=="nosniff"
    assert response.headers["cache-control"]=="no-store"
