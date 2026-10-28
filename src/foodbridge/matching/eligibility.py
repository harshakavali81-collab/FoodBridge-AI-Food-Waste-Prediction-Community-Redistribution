"""Strict matching filters. Never assumes food is medically or legally safe."""
from datetime import datetime,timezone
from .route_cost import haversine_km
def aware(t):
    return t.replace(tzinfo=timezone.utc) if t.tzinfo is None else t.astimezone(timezone.utc)
def eligibility(item,recipient,now=None,max_distance_km=20,quantity_kg=None):
    now=aware(now or datetime.now(timezone.utc))
    reasons=[]
    if not item.food_safety_confirmed: reasons.append("Donor safety acknowledgement missing")
    if aware(item.expires_at)<=now or aware(item.pickup_by)<=now: reasons.append("Expiry or pickup deadline passed")
    if not recipient.verified: reasons.append("Recipient not verified")
    if item.storage_type!=recipient.storage_type: reasons.append("Storage mismatch")
    cats={x.strip().lower() for x in recipient.accepts_categories.split(",")}
    if "all" not in cats and item.category.lower() not in cats: reasons.append("Recipient category mismatch")
    available=max(0,item.quantity_kg-item.allocated_kg)
    amount=min(available,recipient.capacity_kg) if quantity_kg is None else quantity_kg
    if amount<=0 or available<amount or recipient.capacity_kg<amount: reasons.append("Insufficient stock or capacity")
    distance=haversine_km(item.latitude,item.longitude,recipient.latitude,recipient.longitude)
    if distance>max_distance_km: reasons.append("Outside recipient radius")
    return {"eligible":not reasons,"reasons":reasons,"distance_km":round(distance,2),"max_quantity_kg":round(min(available,recipient.capacity_kg),2),"requires_human_confirmation":True}
