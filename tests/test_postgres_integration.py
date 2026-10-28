"""PostgreSQL service integration (CI only); no real food data or cloud instance."""
import os
from datetime import datetime,timezone
import pytest
from sqlalchemy import create_engine,inspect,text,insert
from sqlalchemy.exc import IntegrityError
from backend.app.db.models import PilotReview

@pytest.fixture(scope="module")
def db_engine():
    url=os.getenv("FOODBRIDGE_TEST_POSTGRES_URL")
    if not url:
        pytest.skip("Requires disposable GitHub Actions PostgreSQL service")
    assert url.startswith("postgresql+psycopg://")
    engine=create_engine(url,pool_pre_ping=True)
    yield engine
    engine.dispose()

def test_schema_head_and_foreign_keys(db_engine):
    inspector=inspect(db_engine)
    names=set(inspector.get_table_names())
    assert {"alembic_version","inventory","recipients","donations","audit_events","pilot_reviews"}<=names
    with db_engine.connect() as connection:
        assert connection.scalar(text("SELECT version_num FROM alembic_version"))=="20261028_02"
    unique={col for v in inspector.get_unique_constraints("pilot_reviews") for col in v["column_names"]}
    assert {"tenant_id","check_key"}<=unique
    foreigns={fk["referred_table"] for fk in inspector.get_foreign_keys("donations")}
    assert foreigns=={"inventory","recipients"}

def test_tenant_unique_constraint_on_disposable_postgres(db_engine):
    now=datetime.now(timezone.utc)
    base=dict(check_key="donor_identity",status="accepted_demo",
              evidence_ref="demo:test-evidence",reviewed_by="tester",reviewed_at=now)
    with db_engine.begin() as connection:
        connection.execute(insert(PilotReview),[
            {**base,"tenant_id":"tenant_first"},
            {**base,"tenant_id":"tenant_second"},
        ])
    # Different tenants can review the same check, but duplicate rows within
    # one tenant and check must be rejected by PostgreSQL itself.
    with pytest.raises(IntegrityError):
        with db_engine.begin() as connection:
            connection.execute(insert(PilotReview),{**base,"tenant_id":"tenant_first"})

def test_donation_has_no_fake_approval_or_tenant_claim(db_engine):
    cols={c["name"] for c in inspect(db_engine).get_columns("donations")}
    assert "status" in cols
    assert "tenant_id" not in cols, "Legacy demo donations are deliberately not multi-tenant"
