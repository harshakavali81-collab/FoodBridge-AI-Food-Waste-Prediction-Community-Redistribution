# FoodBridge AI: data integrity and disposable disaster-recovery rehearsal

## Donation ledger reconciliation

Run `PYTHONPATH=.:src python scripts/check_inventory_integrity.py` against a local synthetic demo database.

The read-only report compares:
- Listed inventory `allocated_kg` against the sum of reservations plus demo-confirmed collections.
- Each recipient's capacity against the sum of active reservations across every listing.
- Valid donation masses/statuses and whether collected records include operator name and timestamp.
- Missing references and impossible state transitions.

The command returns exit code **2** when inconsistencies are detected. It doesn't modify records or certify food safety, recipient identity, delivery, or environmental impact. Unit/integration tests intentionally corrupt an isolated SQLite database to verify that it detects errors. Accurate accounting requires separately authenticated human pickup evidence.

## PostgreSQL backup and restore CI

GitHub Actions provisions a throwaway PostgreSQL 17 service, runs the Alembic schema migrations and tests, then:

1. Uses `pg_dump -Fc` inside that matching PostgreSQL container.
2. Restores with `pg_restore --exit-on-error` into a new disposable database.
3. Checks that the expected tables, column names, row counts and migration revision are preserved.
4. Confirms that two fabricated tenant-review records survive the restore.
5. Deletes the restored CI database; no dump file is stored as a GitHub artifact.

The backup script **refuses to run outside GitHub Actions** and only targets the explicitly named localhost test database.

A successful CI restore is **not a production recovery plan**. Actual service readiness still needs scheduled encrypted off-site backups, retention policies, verified key management, least-privilege backup users, point-in-time restore procedures, real recovery-time/recovery-point objectives, and periodic independent disaster-recovery drills under formal approval.

## Release boundaries

- Production operational writes remain blocked.
- The operational inventory and donation tables are not yet tenant-isolated.
- The signed JWT pilot-review workflow is simulation-only and does not authorize real partners.
- No real donor, food handling approval or impact metric is asserted.

## Verified CI outcome (28 October 2026)

The [GitHub Actions workflow run](https://github.com/harshakavali81-collab/FoodBridge-AI-Food-Waste-Prediction-Community-Redistribution/actions/runs/40658684884) succeeded. The Python suite passed **52 tests** (3 PostgreSQL-only tests are skipped in the SQLite runner); the isolated PostgreSQL job passed its 3 database tests, then confirmed a `pg_dump`/`pg_restore` cycle preserved five application tables and the Alembic revision. This is a **disposable, synthetic-only** recovery rehearsal, not an approved or scheduled production backup service.
