"""Migration lifecycle on disposable SQLite only; production data never touched."""
from pathlib import Path
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine,inspect,text
from backend.app.db.database import Base
from backend.app.db import models  # noqa: F401

ROOT=Path(__file__).resolve().parents[1]
def config():
    cfg=Config(str(ROOT/"alembic.ini"))
    cfg.set_main_option("script_location",str(ROOT/"migrations"))
    return cfg

def test_migrate_fresh_database_and_idempotent_reapply(tmp_path,monkeypatch):
    url=f"sqlite:///{tmp_path/'fresh.db'}"
    monkeypatch.setenv("DATABASE_URL",url)
    cfg=config()
    command.upgrade(cfg,"head")
    engine=create_engine(url)
    actual=set(inspect(engine).get_table_names())
    required=set(Base.metadata.tables)
    assert required=={"inventory","recipients","donations","audit_events"}
    assert required <= actual
    for table in Base.metadata.sorted_tables:
        real_cols={col["name"] for col in inspect(engine).get_columns(table.name)}
        assert set(table.columns.keys())==real_cols,table.name
    with engine.connect() as connection:
        version=connection.execute(text("SELECT version_num FROM alembic_version")).scalar()
    assert version=="20261028_01"
    engine.dispose()
    command.upgrade(cfg,"head")
    engine=create_engine(url)
    assert required <= set(inspect(engine).get_table_names())
    engine.dispose()

def test_downgrade_on_throwaway_database_only(tmp_path,monkeypatch):
    url=f"sqlite:///{tmp_path/'demo_drop.db'}"
    monkeypatch.setenv("DATABASE_URL",url)
    cfg=config()
    command.upgrade(cfg,"head")
    command.downgrade(cfg,"base")
    engine=create_engine(url)
    assert not set(Base.metadata.tables).intersection(set(inspect(engine).get_table_names()))
    engine.dispose()
