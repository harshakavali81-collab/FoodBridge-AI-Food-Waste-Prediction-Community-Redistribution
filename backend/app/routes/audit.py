"""Demo event log, not an immutable production compliance audit log."""
from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db.models import AuditEvent
router=APIRouter(prefix="/audit",tags=["demo audit"])

@router.get("")
def recent_events(limit:int=Query(default=50,ge=1,le=100),db:Session=Depends(get_db)):
    events=db.query(AuditEvent).order_by(AuditEvent.id.desc()).limit(limit).all()
    return {"notice":"Non-immutable educational event log, not regulatory evidence",
            "events":[{"id":e.id,"event_type":e.event_type,
                       "entity_type":e.entity_type,"entity_id":e.entity_id,
                       "quantity_kg":e.quantity_kg,"created_at":e.created_at,
                       "demo":e.demo} for e in events]}
