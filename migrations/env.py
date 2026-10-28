"""Alembic migration context with DATABASE_URL override."""
from logging.config import fileConfig
import os
from alembic import context
from sqlalchemy import create_engine,pool
from backend.app.db.database import Base
from backend.app.db import models  # noqa: F401

config=context.config
if config.config_file_name:
    fileConfig(config.config_file_name)
target_metadata=Base.metadata

def database_url():
    return os.environ.get("DATABASE_URL") or config.get_main_option("sqlalchemy.url")

def offline():
    context.configure(url=database_url(),target_metadata=target_metadata,
                      literal_binds=True,dialect_opts={"paramstyle":"named"},compare_type=True)
    with context.begin_transaction():
        context.run_migrations()

def online():
    url=database_url()
    engine=create_engine(url,poolclass=pool.NullPool,
                         connect_args={"check_same_thread":False} if url.startswith("sqlite") else {})
    with engine.connect() as connection:
        context.configure(connection=connection,target_metadata=target_metadata,
                          compare_type=True,render_as_batch=url.startswith("sqlite"))
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()

if context.is_offline_mode():
    offline()
else:
    online()
