# Reviewed initial database migrations (demo / staging)

This is a reproducible **schema migration on a brand-new, empty database**, NOT permission to move real partner data or a claim that production has been deployed.

- `alembic.ini` configures Alembic.
- `migrations/env.py` binds model metadata and uses a runtime `DATABASE_URL`.
- `migrations/versions/20261028_01_initial_schema.py` initializes the four existing SQLAlchemy data tables.
- `scripts/init_schema_for_staging.py` checks staging constraints then applies `upgrade head`.
- `tests/test_migrations.py` tests fresh installation, repeat idempotence and destructive rollback **only on throwaway SQLite**.

Run locally on an empty demo database:

```bash
# bash; Windows PowerShell uses $env:DATABASE_URL = ...
export PYTHONPATH=.:src
export DATABASE_URL=sqlite:///./foodbridge-new-migration-test.db
alembic upgrade head
alembic current
```

Production-style **internal staging** uses PostgreSQL and requires `APP_ENV=production`, `SEED_DEMO_DATA=false`, long server-only `API_KEY`, internal networking, and this command:

```bash
docker compose --env-file .env.staging -f docker-compose.staging.yml run --rm api python scripts/init_schema_for_staging.py
```

Never run this initial revision against a pre-existing SQLite file created with `Base.metadata.create_all()` or existing PostgreSQL schema; doing so tries to create existing tables. First back up the DB, reconcile metadata and schema, review every difference and approve a baseline stamp or custom migration. Do not use `alembic stamp` to hide mismatches.

**Not yet verified:** isolated PostgreSQL end-to-end migration, backup restoration, ongoing schema migration from versions with real records, multi-tenant controls, immutable audit storage or any production environment approval.
