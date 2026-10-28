from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db.models import Recipient
from backend.app.schemas import RecipientCreate,RecipientOut
from backend.app.security import require_write_key
router=APIRouter(prefix="/recipients",tags=["recipients"])
@router.get("",response_model=list[RecipientOut])
def list_recipients(db:Session=Depends(get_db)):
    return db.query(Recipient).order_by(Recipient.id).all()
@router.post("",response_model=RecipientOut,status_code=201,dependencies=[Depends(require_write_key)])
def add_recipient(payload:RecipientCreate,db:Session=Depends(get_db)):
    if db.query(Recipient).filter_by(name=payload.name).first():
        raise HTTPException(409,"Recipient already exists")
    r=Recipient(**payload.model_dump(),demo=False)
    db.add(r);db.commit();db.refresh(r)
    return r
