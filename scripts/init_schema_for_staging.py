"""Manual initial schema bootstrap for a new internal staging database ONLY.
Not a migration framework. No tenant-aware schema or audited data operations.
"""
import os
from backend.app.security import validate_deployment_config
from backend.app.db.database import Base,engine
from backend.app.db import models  # registers metadata
def main():
    validate_deployment_config()
    if os.getenv("APP_ENV") != "production":
        raise SystemExit("This bootstrap is solely for isolated internal staging")
    Base.metadata.create_all(engine)
    print("Internal staging schema initialized; not production-migrated or compliance certified.")
if __name__=="__main__":
    main()
