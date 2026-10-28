"""Evidence-checklist demonstration with signed JWT and tenant-scoped records.

A positive demo evaluation NEVER grants an actual redistribution authorization.
"""
from datetime import datetime, timezone
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.db.models import PilotReview, AuditEvent
from backend.app.identity import Principal, current_principal, has_role
from backend.app.security import require_write_key, production_mode

router=APIRouter(tags=["pilot-readiness"])
CHECKS=(
    "donor_identity",
    "recipient_identity",
    "safe_handling_plan",
    "cold_chain_plan",
    "allergen_traceability",
    "recall_incident_plan",
    "privacy_security_review",
    "pilot_authorization_letter",
)
CheckKey=Literal[
    "donor_identity",
    "recipient_identity",
    "safe_handling_plan",
    "cold_chain_plan",
    "allergen_traceability",
    "recall_incident_plan",
    "privacy_security_review",
    "pilot_authorization_letter",
]

class ReviewInput(BaseModel):
    check_key:CheckKey
    status:Literal["accepted_demo","rejected_demo"]
    evidence_ref:str=Field(pattern=r"^demo:[a-zA-Z0-9/_-]{3,80}$",max_length=85)

def state_for_tenant(db:Session,tenant_id:str):
    records=db.query(PilotReview).filter(PilotReview.tenant_id==tenant_id).all()
    states={r.check_key:{"status":r.status,"reviewer":r.reviewed_by,
                         "evidence_ref":r.evidence_ref,"reviewed_at":r.reviewed_at} for r in records}
    accepted={key for key,v in states.items() if v["status"]=="accepted_demo"}
    reviewers={v["reviewer"] for v in states.values() if v["status"]=="accepted_demo"}
    missing=[key for key in CHECKS if key not in accepted]
    ready=(not missing and len(reviewers)>=2)
    return {
        "tenant_id":tenant_id,
        "checks":{key:states.get(key,{"status":"missing"}) for key in CHECKS},
        "missing_checks":missing,
        "distinct_reviewers":len(reviewers),
        "simulation_ready":ready,
        "authorized_for_real_distribution":False,
        "notice":"Signed reviewers and mock evidence are NOT independent legal or food safety verification.",
    }

@router.get("/identity/me")
def identity_me(principal:Principal=Depends(current_principal)):
    return {"subject":principal.subject,"tenant_id":principal.tenant_id,
            "roles":sorted(principal.roles),"real_food_operations_authorized":False}

@router.get("/pilot/readiness")
def pilot_readiness(principal:Principal=Depends(current_principal),db:Session=Depends(get_db)):
    has_role(principal,{"operator","reviewer","auditor","admin"})
    return state_for_tenant(db,principal.tenant_id)

@router.post("/pilot/reviews",status_code=201,dependencies=[Depends(require_write_key)])
def submit_demo_review(payload:ReviewInput,principal:Principal=Depends(current_principal),db:Session=Depends(get_db)):
    has_role(principal,{"reviewer"})
    if production_mode():
        raise HTTPException(403,"Demo reviews are unavailable in production")
    item=db.query(PilotReview).filter(
        PilotReview.tenant_id==principal.tenant_id,
        PilotReview.check_key==payload.check_key
    ).first()
    if item is None:
        item=PilotReview(tenant_id=principal.tenant_id,check_key=payload.check_key,
                         status=payload.status,evidence_ref=payload.evidence_ref,
                         reviewed_by=principal.subject)
        db.add(item)
    else:
        item.status=payload.status
        item.evidence_ref=payload.evidence_ref
        item.reviewed_by=principal.subject
        item.reviewed_at=datetime.now(timezone.utc)
    db.flush()
    db.add(AuditEvent(event_type="demo_pilot_review",entity_type="pilot_review",
                      entity_id=item.id,demo=True))
    db.commit()
    return {"tenant_id":principal.tenant_id,"check_key":item.check_key,
            "status":item.status,"reviewed_by":item.reviewed_by,
            "real_approval":False}

@router.post("/pilot/evaluate",dependencies=[Depends(require_write_key)])
def simulate_pilot_decision(principal:Principal=Depends(current_principal),db:Session=Depends(get_db)):
    has_role(principal,{"admin"})
    if production_mode():
        raise HTTPException(403,"Pilot simulation cannot authorize production")
    assessment=state_for_tenant(db,principal.tenant_id)
    return {"simulation_outcome":"demo_ready" if assessment["simulation_ready"] else "blocked",
            "missing_checks":assessment["missing_checks"],
            "minimum_two_reviewers_met":assessment["distinct_reviewers"]>=2,
            "authorized_for_real_distribution":False,
            "notice":"Only external legal, safety and accountable human approvals can authorize a real pilot."}
