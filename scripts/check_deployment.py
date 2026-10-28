"""Validate proposed environment before running containers; does not certify security."""
import sys
from dotenv import load_dotenv
from backend.app.security import validate_deployment_config
load_dotenv()
try:
    validate_deployment_config()
except RuntimeError as e:
    print("Configuration rejected:",str(e),file=sys.stderr)
    raise SystemExit(2)
print("Configuration shape accepted. Partner verification, live data, user authentication and security review are still outstanding.")
