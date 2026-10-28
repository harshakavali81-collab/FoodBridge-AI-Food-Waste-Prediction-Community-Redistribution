from test_api import inventory,recipient,seed_pair

BASE="/api/v1"
ADMIN={"X-Demo-Admin-Key":"local-demo-only-administrator-key-123456"}

def post(c,url,data=None,headers=None):
    return c.post(BASE+url,json=data,headers=headers or {})

def test_new_recipient_cannot_claim_verified(client):
    r=post(client,"/recipients",recipient(verified=True))
    assert r.status_code==422
    r=post(client,"/recipients",recipient(verified=False))
    assert r.status_code==201
    assert r.json()["verified"] is False
    assert post(client,f"/recipients/{r.json()['id']}/verify-demo",headers={"X-Demo-Admin-Key":"wrong"}).status_code==403
    assert post(client,f"/recipients/{r.json()['id']}/verify-demo",headers=ADMIN).json()["verified"] is True
    assert post(client,f"/recipients/{r.json()['id']}/verify-demo",headers=ADMIN).status_code==200

def test_recipient_capacity_aggregated_across_listings(client):
    first=post(client,"/inventory",inventory()).json()["id"]
    second=post(client,"/inventory",inventory(food_name="Another bread batch")).json()["id"]
    r=post(client,"/recipients",recipient(verified=False,capacity_kg=10)).json()["id"]
    assert post(client,f"/recipients/{r}/verify-demo",headers=ADMIN).status_code==200
    a=post(client,"/donations",{"inventory_id":first,"recipient_id":r,"quantity_kg":7})
    assert a.status_code==201,a.text
    match=client.get(BASE+f"/matches/{second}").json()["eligible_matches"]
    assert len(match)==1 and match[0]["max_quantity_kg"]==3
    b=post(client,"/donations",{"inventory_id":second,"recipient_id":r,"quantity_kg":5})
    assert b.status_code==409,b.text
    assert post(client,f"/donations/{a.json()['id']}/cancel").status_code==200
    assert post(client,"/donations",{"inventory_id":second,"recipient_id":r,"quantity_kg":10}).status_code==201

def test_collected_reservation_frees_recipient_hold(client):
    i,r=seed_pair(client)
    first=post(client,"/donations",{"inventory_id":i,"recipient_id":r,"quantity_kg":15})
    assert first.status_code==201
    assert post(client,"/donations",{"inventory_id":i,"recipient_id":r,"quantity_kg":1}).status_code in (409,422)
    confirm=post(client,f"/donations/{first.json()['id']}/confirm",{"confirmed_by":"Local Demo Operator"})
    assert confirm.status_code==200
    assert post(client,"/donations",{"inventory_id":i,"recipient_id":r,"quantity_kg":1}).status_code==201

def test_event_log_tracks_actions_without_personal_data(client):
    i,r=seed_pair(client)
    created=post(client,"/donations",{"inventory_id":i,"recipient_id":r,"quantity_kg":4})
    assert created.status_code==201
    assert post(client,f"/donations/{created.json()['id']}/cancel").status_code==200
    events=client.get(BASE+"/audit").json()["events"]
    types={event["event_type"] for event in events}
    assert {"recipient_created","recipient_demo_verified","donation_reserved","donation_cancelled"}<=types
    assert all("pickup_confirmed_by" not in e for e in events)
    assert all(e["demo"] for e in events if e["event_type"]!="inventory_created")

def test_prevent_negative_inventory_after_duplicate_cancel(client):
    i,r=seed_pair(client)
    donation=post(client,"/donations",{"inventory_id":i,"recipient_id":r,"quantity_kg":6}).json()
    assert post(client,f"/donations/{donation['id']}/cancel").status_code==200
    assert post(client,f"/donations/{donation['id']}/cancel").status_code==409
    listed=client.get(BASE+"/inventory").json()
    assert listed[0]["allocated_kg"]==0
