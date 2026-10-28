"""Recipient registry. API submissions cannot self-approve.
The demo-only verification endpoint is NOT independent charity due diligence.
"""
import os
import secrets
from fastapi import APIRouter,Depends,HTTPException,Header
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db.models import Recipient,AuditEvent
from backend.app.schemas import RecipientCreate,RecipientOut
from backend.app.security import require_write_key,production_mode

router=APIRouter(prefix="/recipients",tags=["recipients"])

@router.get("",response_model=list[RecipientOut])
def list_recipients(db:Session=Depends(get_db)):
    return db.query(Recipient).order_by(Recipient.id).all()

@router.post("",response_model=RecipientOut,status_code=201,dependencies=[Depends(require_write_key)])
def add_recipient(payload:RecipientCreate,db:Session=Depends(get_db)):
    if payload.verified:
        raise HTTPException(422,"Self-verification is forbidden: new recipient records must start unverified")
    if db.query(Recipient).filter_by(name=payload.name).first():
        raise HTTPException(409,"Recipient already exists")
    r=Recipient(**payload.model_dump(exclude={"verified"}),verified=False,demo=True)
    db.add(r)
    db.flush()
    db.add(AuditEvent(event_type="recipient_created",entity_type="recipient",entity_id=r.id,demo=True))
    db.commit()
    db.refresh(r)
    return r

@router.post("/{recipient_id}/verify-demo",response_model=RecipientOut,dependencies=[Depends(require_write_key)])
def verify_demo_recipient(recipient_id:int,x_demo_admin_key:str|None=Header(default=None),db:Session=Depends(get_db)):
    # A development-only teaching action. Never label this independent partner validation.
    key=os.getenv("DEMO_ADMIN_KEY","")
    if production_mode() or len(key)<16 or not x_demo_admin_key or not secrets.compare_digest(key,x_demo_admin_key):
        raise HTTPException(403,"Demo verification restricted to a configured local administrator")
    r=db.get(Recipient,recipient_id)
    if not r:raise HTTPException(404,"Recipient not found")
    if not r.demo:raise HTTPException(403,"Only fictional demo recipients may be demo-verified")
    if not r.verified:
        r.verified=True
        db.add(AuditEvent(event_type="recipient_demo_verified",entity_type="recipient",entity_id=r.id,demo=True))
        db.commit()
    db.refresh(r)
    return r
