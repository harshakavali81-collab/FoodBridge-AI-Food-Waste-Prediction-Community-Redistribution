import os
import secrets
from fastapi import Header,HTTPException
def require_write_key(x_api_key: str|None=Header(default=None)):
    key=os.getenv("API_KEY","")
    if not key:
        if os.getenv("APP_ENV","development").lower()=="production":
            raise HTTPException(503,"Production API_KEY not configured")
        return
    if not x_api_key or not secrets.compare_digest(x_api_key,key):
        raise HTTPException(401,"Missing or invalid API key")
