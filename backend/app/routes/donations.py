"""Atomic inventory/recipient-capacity reservations with safe state transitions.

The flow is educational only. It cannot certify real food, charities or pickups.
"""
import os
from datetime import datetime,timezone
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import update,select,func
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db.models import Inventory,Recipient,Donation,AuditEvent
from backend.app.schemas import DonationCreate,DonationOut,ConfirmPickup
from backend.app.security import require_write_key
from foodbridge.matching.eligibility import eligibility
from foodbridge.matching.match_donations import ranked_matches

router=APIRouter(tags=["donations"])

def reserved_capacity(db:Session,recipient_id:int)->float:
    return float(db.scalar(select(func.coalesce(func.sum(Donation.quantity_kg),0.0)).where(
        Donation.recipient_id==recipient_id,Donation.status=="reserved")) or 0)

@router.get("/matches/{inventory_id}")
def matches(inventory_id:int,db:Session=Depends(get_db)):
    item=db.get(Inventory,inventory_id)
    if item is None:raise HTTPException(404,"Inventory not found")
    recipients=db.query(Recipient).all()
    holds={r.id:reserved_capacity(db,r.id) for r in recipients}
    candidates=ranked_matches(item,recipients,float(os.getenv("MAX_MATCH_DISTANCE_KM","20")),holds)
    return {"inventory_id":inventory_id,"eligible_matches":candidates,"notice":"Demo candidates only, not independent food safety or partner verification."}

@router.get("/donations",response_model=list[DonationOut])
def list_donations(db:Session=Depends(get_db)):
    return db.query(Donation).order_by(Donation.id.desc()).all()

@router.post("/donations",response_model=DonationOut,status_code=201,dependencies=[Depends(require_write_key)])
def reserve_donation(payload:DonationCreate,db:Session=Depends(get_db)):
    item=db.get(Inventory,payload.inventory_id)
    recipient=db.get(Recipient,payload.recipient_id)
    if not item or not recipient:raise HTTPException(404,"Inventory or recipient not found")
    check=eligibility(item,recipient,quantity_kg=payload.quantity_kg,
                      max_distance_km=float(os.getenv("MAX_MATCH_DISTANCE_KM","20")))
    if not check["eligible"]:
        raise HTTPException(422,{"reasons":check["reasons"]})

    # Serialize all reservations for the same recipient before checking total
    # outstanding holds. In PostgreSQL READ COMMITTED the no-op row update locks
    # the recipient until commit; SQLite serializes writers as well.
    db.execute(update(Recipient).where(Recipient.id==recipient.id).values(capacity_kg=Recipient.capacity_kg))
    remaining=recipient.capacity_kg-reserved_capacity(db,recipient.id)
    if payload.quantity_kg>remaining+1e-7:
        db.rollback()
        raise HTTPException(409,"Recipient capacity already held by other reservations")
    result=db.execute(update(Inventory).where(
        Inventory.id==item.id,
        Inventory.allocated_kg+payload.quantity_kg<=Inventory.quantity_kg,
        Inventory.pickup_by>datetime.now(timezone.utc),
        Inventory.expires_at>datetime.now(timezone.utc),
        Inventory.food_safety_confirmed.is_(True)
    ).values(allocated_kg=Inventory.allocated_kg+payload.quantity_kg))
    if result.rowcount!=1:
        db.rollback()
        raise HTTPException(409,"Stock no longer eligible or already reserved")
    d=Donation(inventory_id=item.id,recipient_id=recipient.id,
               quantity_kg=payload.quantity_kg,status="reserved",
               demo=item.demo or recipient.demo)
    db.add(d)
    db.flush()
    db.add(AuditEvent(event_type="donation_reserved",entity_type="donation",
                      entity_id=d.id,quantity_kg=d.quantity_kg,demo=d.demo))
    db.commit()
    db.refresh(d)
    return d

@router.post("/donations/{donation_id}/confirm",response_model=DonationOut,dependencies=[Depends(require_write_key)])
def confirm_pickup(donation_id:int,payload:ConfirmPickup,db:Session=Depends(get_db)):
    d=db.get(Donation,donation_id)
    if not d:raise HTTPException(404,"Donation not found")
    # Only one successful transition is allowed under simultaneous requests.
    result=db.execute(update(Donation).where(
        Donation.id==donation_id,Donation.status=="reserved"
    ).values(status="collected",pickup_confirmed_by=payload.confirmed_by,
             collected_at=datetime.now(timezone.utc)))
    if result.rowcount!=1:
        db.rollback()
        raise HTTPException(409,"Only reserved donations can be confirmed")
    db.add(AuditEvent(event_type="pickup_confirmed",entity_type="donation",
                      entity_id=donation_id,quantity_kg=d.quantity_kg,demo=d.demo))
    db.commit()
    db.refresh(d)
    return d

@router.post("/donations/{donation_id}/cancel",response_model=DonationOut,dependencies=[Depends(require_write_key)])
def cancel(donation_id:int,db:Session=Depends(get_db)):
    d=db.get(Donation,donation_id)
    if not d:raise HTTPException(404,"Donation not found")
    result=db.execute(update(Donation).where(
        Donation.id==donation_id,Donation.status=="reserved"
    ).values(status="cancelled"))
    if result.rowcount!=1:
        db.rollback()
        raise HTTPException(409,"Only reserved donations can be cancelled")
    db.execute(update(Inventory).where(Inventory.id==d.inventory_id).values(
        allocated_kg=Inventory.allocated_kg-d.quantity_kg))
    db.add(AuditEvent(event_type="donation_cancelled",entity_type="donation",
                      entity_id=donation_id,quantity_kg=d.quantity_kg,demo=d.demo))
    db.commit()
    db.refresh(d)
    return d
