"""Read-only conservation checks for the synthetic-data donation ledger.

The report is an integrity diagnostic, NOT proof that real food was delivered,
that a receiving organization is legitimate, or that the food was safe.
"""
from collections import defaultdict
from math import isfinite
from sqlalchemy.orm import Session
from backend.app.db.models import Inventory, Recipient, Donation

TOLERANCE_KG=0.00001
VALID_STATUSES={"reserved","collected","cancelled"}

def is_nonnegative_number(value):
    try:
        number=float(value)
        return isfinite(number) and number >= 0
    except (TypeError,ValueError,OverflowError):
        return False

def check_ledger(db:Session)->dict:
    inventory=db.query(Inventory).all()
    recipients=db.query(Recipient).all()
    donations=db.query(Donation).all()
    issues=[]
    stock_used=defaultdict(float)
    held_by_recipient=defaultdict(float)
    items_by_id={item.id:item for item in inventory}
    recipients_by_id={item.id:item for item in recipients}

    for item in inventory:
        if not is_nonnegative_number(item.quantity_kg) or not is_nonnegative_number(item.allocated_kg):
            issues.append(f"inventory:{item.id}:invalid_mass")
            continue
        if item.allocated_kg>item.quantity_kg+TOLERANCE_KG:
            issues.append(f"inventory:{item.id}:overallocated")

    for recipient in recipients:
        if not is_nonnegative_number(recipient.capacity_kg):
            issues.append(f"recipient:{recipient.id}:invalid_capacity")

    for donation in donations:
        if not is_nonnegative_number(donation.quantity_kg) or donation.quantity_kg<=0:
            issues.append(f"donation:{donation.id}:invalid_mass")
            continue
        if donation.inventory_id not in items_by_id:
            issues.append(f"donation:{donation.id}:missing_inventory")
        if donation.recipient_id not in recipients_by_id:
            issues.append(f"donation:{donation.id}:missing_recipient")
        if donation.status not in VALID_STATUSES:
            issues.append(f"donation:{donation.id}:invalid_status")
            continue
        if donation.status in ("reserved","collected"):
            stock_used[donation.inventory_id]+=donation.quantity_kg
        if donation.status=="reserved":
            held_by_recipient[donation.recipient_id]+=donation.quantity_kg
            if donation.collected_at is not None or donation.pickup_confirmed_by:
                issues.append(f"donation:{donation.id}:premature_pickup_confirmation")
        if donation.status=="collected":
            if donation.collected_at is None or not donation.pickup_confirmed_by:
                issues.append(f"donation:{donation.id}:missing_human_pickup_confirmation")
        if donation.status=="cancelled":
            if donation.collected_at is not None:
                issues.append(f"donation:{donation.id}:cancelled_after_collection")

    for item in inventory:
        if is_nonnegative_number(item.allocated_kg) and abs(float(item.allocated_kg)-stock_used[item.id])>TOLERANCE_KG:
            issues.append(f"inventory:{item.id}:allocation_ledger_mismatch")
    for recipient in recipients:
        if is_nonnegative_number(recipient.capacity_kg) and held_by_recipient[recipient.id]>recipient.capacity_kg+TOLERANCE_KG:
            issues.append(f"recipient:{recipient.id}:reserved_capacity_exceeded")

    return {
        "ok":not issues,
        "issues":sorted(set(issues)),
        "inventory_records":len(inventory),
        "recipient_records":len(recipients),
        "donation_records":len(donations),
        "scope":"Synthetic demonstration ledger; not food safety or impact certification",
    }
