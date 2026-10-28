"""Upgrade isolated internal staging using reviewed Alembic revisions.

Never point this at a real partner database without independent backup,
schema-diff review and an authorized release plan. Writes remain disabled.
"""
import os
from pathlib import Path
from alembic import command
from alembic.config import Config
from backend.app.security import validate_deployment_config

def main():
    validate_deployment_config()
    if os.getenv("APP_ENV") != "production":
        raise SystemExit("This migration bootstrap is for isolated internal staging only")
    root=Path(__file__).resolve().parents[1]
    config=Config(str(root/"alembic.ini"))
    config.set_main_option("script_location",str(root/"migrations"))
    command.upgrade(config,"head")
    print("Internal staging database migrated to head. Production writes remain disabled.")

if __name__ == "__main__":
    main()
