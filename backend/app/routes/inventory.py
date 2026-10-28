from datetime import datetime,timezone
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db.models import Inventory
from backend.app.schemas import InventoryCreate,InventoryOut
from backend.app.security import require_write_key
router=APIRouter(prefix="/inventory",tags=["inventory"])
@router.get("",response_model=list[InventoryOut])
def list_inventory(db:Session=Depends(get_db)):
    return db.query(Inventory).order_by(Inventory.id.desc()).all()
@router.post("",response_model=InventoryOut,status_code=201,dependencies=[Depends(require_write_key)])
def create_inventory(payload:InventoryCreate,db:Session=Depends(get_db)):
    if payload.expires_at<=datetime.now(timezone.utc) or payload.pickup_by<=datetime.now(timezone.utc):
        raise HTTPException(422,"Expiry and pickup deadlines must be future dates")
    item=Inventory(**payload.model_dump(),demo=False)
    db.add(item);db.commit();db.refresh(item)
    return item
