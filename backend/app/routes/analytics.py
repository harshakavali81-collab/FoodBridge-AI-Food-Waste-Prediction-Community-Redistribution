"""Synthetic CSV for analytical trends; confirmed operational collections from DB."""
import csv,io
from collections import defaultdict
from pathlib import Path
from fastapi import APIRouter,Depends,Response
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db.models import Inventory,Recipient,Donation
router=APIRouter(tags=["analytics"])
CSV=Path(__file__).resolve().parents[3]/"data"/"synthetic"/"daily_operations.csv"
def history():
    if not CSV.exists():
        return []
    with CSV.open(newline="") as f:
        return list(csv.DictReader(f))
@router.get("/dashboard")
def dashboard(db:Session=Depends(get_db)):
    items=db.query(Inventory).all();donations=db.query(Donation).all()
    return {"demo_data":any(x.demo for x in items),"active_listings":len(items),"total_listed_kg":round(sum(x.quantity_kg for x in items),2),"available_kg":round(sum(max(0,x.quantity_kg-x.allocated_kg) for x in items),2),"reserved_kg":round(sum(x.quantity_kg for x in donations if x.status=="reserved"),2),"confirmed_collected_kg":round(sum(x.quantity_kg for x in donations if x.status=="collected"),2),"verified_recipients":db.query(Recipient).filter_by(verified=True).count(),"note":"Listings and reservations are not confirmed pickups."}
@router.get("/analytics/trends")
def trends():
    daily=defaultdict(lambda:{"date":"","surplus_kg":0.,"sold_kg":0.,"donated_kg":0.})
    cat=defaultdict(float)
    for r in history():
        v=daily[r["date"]];v["date"]=r["date"]
        for k in ("surplus_kg","sold_kg","donated_kg"): v[k]+=float(r[k])
        cat[r["category"]]+=float(r["surplus_kg"])
    return {"data_source":"synthetic_demo_history","daily":[{k:round(v,1) if isinstance(v,float) else v for k,v in a.items()} for a in sorted(daily.values(),key=lambda x:x["date"])[-30:]],"by_category":[{"name":k,"value":round(v,1)} for k,v in sorted(cat.items())]}
@router.get("/analytics/export.csv")
def export():
    rows=history()
    if not rows:return Response(content="",media_type="text/csv")
    buf=io.StringIO();w=csv.DictWriter(buf,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    return Response(content=buf.getvalue(),media_type="text/csv",headers={"Content-Disposition":'attachment; filename="foodbridge_synthetic_operations.csv"'})
@router.get("/forecast/preview")
def preview():
    sums=defaultdict(float)
    for r in history():sums[r["date"]]+=float(r["surplus_kg"])
    vals=[sums[k] for k in sorted(sums)]
    return {"prediction_type":"7-day moving average baseline","source":"synthetic_demo_history","estimated_daily_surplus_kg":round(sum(vals[-7:])/max(1,len(vals[-7:])),1),"model_trained":False,"note":"Offline illustrative estimate only. Actual available food requires human entry."}
