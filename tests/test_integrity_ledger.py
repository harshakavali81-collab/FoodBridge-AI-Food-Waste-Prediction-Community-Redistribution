"""Conservation checks on isolated synthetic API fixtures."""
from sqlalchemy import update
from backend.app.db.database import get_db
from backend.app.db.models import Inventory,Recipient,Donation
from backend.app.main import app
from foodbridge.monitoring.ledger import check_ledger
from test_api import seed_pair

def session_from_client():
    # The TestClient fixture installs an isolated SQLite StaticPool override.
    override=app.dependency_overrides[get_db]
    generator=override()
    session=next(generator)
    return generator,session

def inspect_ledger():
    gen,session=session_from_client()
    try:
        return check_ledger(session)
    finally:
        gen.close()

def test_empty_synthetic_ledger_is_consistent(client):
    result=inspect_ledger()
    assert result["ok"] is True
    assert result["donation_records"]==0

def test_reservation_collection_and_cancel_conserve_mass(client):
    inventory,recipient=seed_pair(client)
    reserve=client.post("/api/v1/donations",json={
        "inventory_id":inventory,"recipient_id":recipient,"quantity_kg":6
    })
    assert reserve.status_code==201,reserve.text
    assert inspect_ledger()["ok"] is True
    donation_id=reserve.json()["id"]
    assert client.post(f"/api/v1/donations/{donation_id}/confirm",json={
        "confirmed_by":"Synthetic Operator"
    }).status_code==200
    assert inspect_ledger()["ok"] is True
    assert inspect_ledger()["donation_records"]==1

def test_detects_manually_corrupted_inventory_allocation(client):
    inventory,recipient=seed_pair(client)
    gen,session=session_from_client()
    try:
        session.execute(update(Inventory).where(Inventory.id==inventory).values(allocated_kg=11))
        session.commit()
    finally:
        gen.close()
    report=inspect_ledger()
    assert report["ok"] is False
    assert f"inventory:{inventory}:allocation_ledger_mismatch" in report["issues"]

def test_detects_overbooked_recipient_capacity(client):
    inventory,recipient=seed_pair(client)
    donation=client.post("/api/v1/donations",json={
        "inventory_id":inventory,"recipient_id":recipient,"quantity_kg":8
    })
    assert donation.status_code==201
    gen,session=session_from_client()
    try:
        session.execute(update(Recipient).where(Recipient.id==recipient).values(capacity_kg=3))
        session.commit()
    finally:
        gen.close()
    report=inspect_ledger()
    assert f"recipient:{recipient}:reserved_capacity_exceeded" in report["issues"]

def test_detects_invalid_collection_state(client):
    inventory,recipient=seed_pair(client)
    donation=client.post("/api/v1/donations",json={
        "inventory_id":inventory,"recipient_id":recipient,"quantity_kg":4
    })
    assert donation.status_code==201
    gen,session=session_from_client()
    try:
        session.execute(update(Donation).where(Donation.id==donation.json()["id"]).values(status="collected"))
        session.commit()
    finally:
        gen.close()
    report=inspect_ledger()
    assert not report["ok"]
    assert any("missing_human_pickup_confirmation" in msg for msg in report["issues"])
