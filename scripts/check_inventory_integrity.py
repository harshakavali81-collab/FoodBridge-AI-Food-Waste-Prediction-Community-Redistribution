"""Read-only integrity command for synthetic development and isolated staging.

Exits nonzero when stock conservation, status, or reserved capacity is broken.
NEVER uses this result as a food handling approval or an impact certificate.
"""
import json
import sys
from backend.app.db.database import SessionLocal
from foodbridge.monitoring.ledger import check_ledger

def main():
    with SessionLocal() as session:
        report=check_ledger(session)
    print(json.dumps(report,indent=2))
    return 0 if report["ok"] else 2

if __name__=="__main__":
    sys.exit(main())
