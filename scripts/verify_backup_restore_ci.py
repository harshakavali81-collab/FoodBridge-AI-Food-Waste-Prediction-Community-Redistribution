"""CI-ONLY disposable PostgreSQL dump/restore with data and schema verification.

Never operates on a non-CI server. Never uploads backups as artifacts.
This proves a basic local restore path, not production encrypted backup policy.
"""
import os
import re
import subprocess
from sqlalchemy import create_engine,inspect,text
from sqlalchemy.engine import make_url

TABLES=("inventory","recipients","donations","audit_events","pilot_reviews","alembic_version")
RESTORED="foodbridge_restore_ci"

def run(command,*,input_bytes=None):
    completed=subprocess.run(command,input=input_bytes,stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,check=True)
    return completed.stdout

def main():
    container=os.getenv("PG_SERVICE_ID","")
    value=os.getenv("FOODBRIDGE_TEST_POSTGRES_URL","")
    if (os.getenv("GITHUB_ACTIONS")!="true" or not re.fullmatch(r"[0-9a-f]{12,64}",container)
            or not value.startswith("postgresql+psycopg://")
            or make_url(value).database!="foodbridge_test"
            or make_url(value).host!="localhost"):
        raise SystemExit("Refusing backup/restore outside isolated GitHub CI database")
    def docker(*args,input_bytes=None):
        return run(["docker","exec",*(["-i"] if input_bytes is not None else []),
                    container,*args],input_bytes=input_bytes)
    dump=docker("pg_dump","-U","fb_test","-d","foodbridge_test",
                "-Fc","--no-owner","--no-acl")
    if len(dump)<512:
        raise RuntimeError("Unexpectedly empty PostgreSQL backup")
    original=create_engine(value,pool_pre_ping=True)
    target_url=make_url(value).set(database=RESTORED)
    restored=create_engine(target_url,pool_pre_ping=True)
    try:
        docker("createdb","-U","fb_test",RESTORED)
        docker("pg_restore","-U","fb_test","-d",RESTORED,
               "--no-owner","--no-acl","--exit-on-error",input_bytes=dump)
        src_tables=set(inspect(original).get_table_names())
        dst_tables=set(inspect(restored).get_table_names())
        if not set(TABLES).issubset(src_tables&dst_tables):
            raise AssertionError("Missing required tables in source or restored schema")
        summary={}
        for table in TABLES:
            # Table names are fixed constants, never user-controlled.
            with original.connect() as src,restored.connect() as dst:
                before=src.scalar(text(f'SELECT count(*) FROM "{table}"'))
                after=dst.scalar(text(f'SELECT count(*) FROM "{table}"'))
            if before!=after:
                raise AssertionError(f"Restore row-count mismatch: {table}")
            source_columns={c["name"] for c in inspect(original).get_columns(table)}
            restored_columns={c["name"] for c in inspect(restored).get_columns(table)}
            if source_columns!=restored_columns:
                raise AssertionError(f"Restore schema mismatch: {table}")
            summary[table]=before
        if summary["pilot_reviews"]<2:
            raise AssertionError("Expected two synthetic cross-tenant review records")
        with restored.connect() as db:
            version=db.scalar(text("SELECT version_num FROM alembic_version"))
        if version!="20261028_02":
            raise AssertionError("Restored migration revision mismatch")
        print("Disposable PostgreSQL dump/restore verified. Rows by table:",summary)
    finally:
        original.dispose()
        restored.dispose()
        # Container is a disposable Actions service; the restored DB is test-only.
        docker("dropdb","-U","fb_test",RESTORED)

if __name__=="__main__":
    main()
