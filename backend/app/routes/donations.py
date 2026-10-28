"""Donation reservation and confirmation. Human review remains required."""
import os
from datetime import datetime,timezone
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db.models import Inventory,Recipient,Donation
from backend.app.schemas import DonationCreate,DonationOut,ConfirmPickup
from backend.app.security import require_write_key
from foodbridge.matching.eligibility import eligibility
from foodbridge.matching.match_donations import ranked_matches
router=APIRouter(tags=["donations"])
@router.get("/matches/{inventory_id}")
def matches(inventory_id:int,db:Session=Depends(get_db)):
    item=db.get(Inventory,inventory_id)
    if item is None: raise HTTPException(404,"Inventory not found")
    m=ranked_matches(item,db.query(Recipient).all(),float(os.getenv("MAX_MATCH_DISTANCE_KM","20")))
    return {"inventory_id":inventory_id,"eligible_matches":m,"notice":"Candidates only, not certified food-safe."}
@router.get("/donations",response_model=list[DonationOut])
def list_donations(db:Session=Depends(get_db)):
    return db.query(Donation).order_by(Donation.id.desc()).all()
@router.post("/donations",response_model=DonationOut,status_code=201,dependencies=[Depends(require_write_key)])
def reserve_donation(payload:DonationCreate,db:Session=Depends(get_db)):
    item=db.get(Inventory,payload.inventory_id)
    recipient=db.get(Recipient,payload.recipient_id)
    if not item or not recipient: raise HTTPException(404,"Inventory or recipient not found")
    check=eligibility(item,recipient,quantity_kg=payload.quantity_kg,max_distance_km=float(os.getenv("MAX_MATCH_DISTANCE_KM","20")))
    if not check["eligible"]: raise HTTPException(422,{"reasons":check["reasons"]})
    result=db.execute(update(Inventory).where(Inventory.id==item.id, Inventory.allocated_kg+payload.quantity_kg<=Inventory.quantity_kg).values(allocated_kg=Inventory.allocated_kg+payload.quantity_kg))
    if result.rowcount!=1:
        db.rollback();raise HTTPException(409,"Stock already reserved")
    donation=Donation(inventory_id=item.id,recipient_id=recipient.id,quantity_kg=payload.quantity_kg,status="reserved",demo=item.demo or recipient.demo)
    db.add(donation);db.commit();db.refresh(donation)
    return donation
@router.post("/donations/{donation_id}/confirm",response_model=DonationOut,dependencies=[Depends(require_write_key)])
def confirm_pickup(donation_id:int,payload:ConfirmPickup,db:Session=Depends(get_db)):
    d=db.get(Donation,donation_id)
    if not d: raise HTTPException(404,"Donation not found")
    if d.status!="reserved": raise HTTPException(409,"Only reserved donations can be confirmed")
    d.status="collected";d.pickup_confirmed_by=payload.confirmed_by;d.collected_at=datetime.now(timezone.utc)
    db.commit();db.refresh(d);return d
@router.post("/donations/{donation_id}/cancel",response_model=DonationOut,dependencies=[Depends(require_write_key)])
def cancel(donation_id:int,db:Session=Depends(get_db)):
    d=db.get(Donation,donation_id)
    if not d: raise HTTPException(404,"Donation not found")
    if d.status!="reserved": raise HTTPException(409,"Only reserved donations can be cancelled")
    d.status="cancelled"
    db.execute(update(Inventory).where(Inventory.id==d.inventory_id).values(allocated_kg=Inventory.allocated_kg-d.quantity_kg))
    db.commit();db.refresh(d);return d
