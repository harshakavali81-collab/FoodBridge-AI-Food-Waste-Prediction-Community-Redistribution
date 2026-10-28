"""Offline OIDC/JWT validation for the **non-operational** pilot-review sandbox.

No passwords are collected. No unsigned tokens, HS256 secrets or caller-supplied
tenant headers are accepted. A real service additionally requires identity-provider
provisioning, key rotation, revocation, tenant onboarding and independent audit.
"""
import os
import re
from dataclasses import dataclass
from typing import FrozenSet

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer=HTTPBearer(auto_error=False)
TENANT_PATTERN=re.compile(r"^[a-zA-Z0-9_-]{2,64}$")
ROLE_SET=frozenset({"operator","reviewer","auditor","admin"})

@dataclass(frozen=True)
class Principal:
    subject: str
    tenant_id: str
    roles: FrozenSet[str]

def decode_identity(raw_token: str)->Principal:
    public_key=os.getenv("OIDC_PUBLIC_KEY_PEM","").replace("\\n","\n")
    issuer=os.getenv("OIDC_ISSUER","")
    audience=os.getenv("OIDC_AUDIENCE","")
    if not public_key.strip() or not issuer or not audience:
        raise HTTPException(503,"Signed identity provider is not configured")
    try:
        claims=jwt.decode(
            raw_token,
            public_key,
            algorithms=["RS256"],
            issuer=issuer,
            audience=audience,
            leeway=15,
            options={"require":["exp","iat","iss","aud","sub"]},
        )
    except (jwt.PyJWTError,ValueError,TypeError):
        raise HTTPException(401,"Invalid or expired signed identity")
    subject=claims.get("sub")
    tenant=claims.get("tenant_id")
    roles=claims.get("roles")
    if not isinstance(subject,str) or not (2<=len(subject)<=128):
        raise HTTPException(403,"Invalid identity subject")
    if not isinstance(tenant,str) or not TENANT_PATTERN.fullmatch(tenant):
        raise HTTPException(403,"Missing or invalid tenant assignment")
    if not isinstance(roles,list) or not roles or any(not isinstance(x,str) for x in roles):
        raise HTTPException(403,"Missing role assignment")
    selected=frozenset(roles)
    if not selected.issubset(ROLE_SET):
        raise HTTPException(403,"Unsupported role assignment")
    return Principal(subject=subject,tenant_id=tenant,roles=selected)

def current_principal(credentials:HTTPAuthorizationCredentials|None=Depends(bearer))->Principal:
    if credentials is None or credentials.scheme.lower()!="bearer":
        raise HTTPException(401,"Signed Bearer token required")
    return decode_identity(credentials.credentials)

def has_role(principal:Principal,roles:set[str])->None:
    if not principal.roles.intersection(roles):
        raise HTTPException(403,"Role not authorized for this action")
