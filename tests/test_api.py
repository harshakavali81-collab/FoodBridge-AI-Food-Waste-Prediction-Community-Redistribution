from datetime import datetime,timezone,timedelta
def inventory(**kw):
    t=datetime.now(timezone.utc)
    v=dict(partner_name="Demo Kitchen",food_name="Wheat rolls",category="bakery",quantity_kg=20,storage_type="ambient",allergen_info="Wheat",food_safety_confirmed=True,safety_notes="Donor human reviewed",expires_at=(t+timedelta(days=2)).isoformat(),pickup_by=(t+timedelta(days=1)).isoformat(),latitude=17.4,longitude=78.47)
    v.update(kw);return v
def recipient(**kw):
    v=dict(name="Aid Demo",verified=False,capacity_kg=15,accepts_categories="bakery",storage_type="ambient",latitude=17.41,longitude=78.48)
    v.update(kw);return v
def seed_pair(c):
    a=c.post("/api/v1/inventory",json=inventory());b=c.post("/api/v1/recipients",json=recipient())
    assert a.status_code==201 and b.status_code==201
    r_id=b.json()["id"]
    check=c.post(f"/api/v1/recipients/{r_id}/verify-demo",headers={"X-Demo-Admin-Key":"local-demo-only-administrator-key-123456"})
    assert check.status_code==200,check.text
    return a.json()["id"],r_id
def test_health(client):
    assert client.get("/api/v1/health").json()["status"]=="ok"
    assert client.get("/api/v1/dashboard").json()["confirmed_collected_kg"]==0
def test_match_and_pickup(client):
    i,r=seed_pair(client);assert client.get(f"/api/v1/matches/{i}").json()["eligible_matches"][0]["recipient_id"]==r
    d=client.post("/api/v1/donations",json={"inventory_id":i,"recipient_id":r,"quantity_kg":8})
    assert d.status_code==201,d.text
    assert client.get("/api/v1/dashboard").json()["reserved_kg"]==8
    assert client.get("/api/v1/dashboard").json()["confirmed_collected_kg"]==0
    url=f"/api/v1/donations/{d.json()['id']}/confirm"
    assert client.post(url,json={"confirmed_by":"Demo operator"}).status_code==200
    assert client.post(url,json={"confirmed_by":"Again"}).status_code==409
    assert client.get("/api/v1/dashboard").json()["confirmed_collected_kg"]==8
def test_unsafe_and_expired(client):
    i=client.post("/api/v1/inventory",json=inventory(food_safety_confirmed=False)).json()["id"]
    r=client.post("/api/v1/recipients",json=recipient()).json()["id"]
    assert client.get(f"/api/v1/matches/{i}").json()["eligible_matches"]==[]
    assert client.post("/api/v1/donations",json={"inventory_id":i,"recipient_id":r,"quantity_kg":2}).status_code==422
    past=datetime.now(timezone.utc)-timedelta(days=1)
    assert client.post("/api/v1/inventory",json=inventory(expires_at=past.isoformat(),pickup_by=past.isoformat())).status_code==422
def test_overallocation_and_cancel(client):
    i,r=seed_pair(client)
    assert client.post("/api/v1/donations",json={"inventory_id":i,"recipient_id":r,"quantity_kg":14}).status_code==201
    assert client.post("/api/v1/donations",json={"inventory_id":i,"recipient_id":r,"quantity_kg":14}).status_code==422
    d=client.get("/api/v1/donations").json()[0]
    url=f"/api/v1/donations/{d['id']}/cancel"
    assert client.post(url).status_code==200
    assert client.post(url).status_code==409
    assert client.get("/api/v1/dashboard").json()["available_kg"]==20
def test_bad_recipient_and_validation(client):
    i=client.post("/api/v1/inventory",json=inventory()).json()["id"]
    r=client.post("/api/v1/recipients",json=recipient(storage_type="frozen",verified=False)).json()["id"]
    assert client.post("/api/v1/donations",json={"inventory_id":i,"recipient_id":r,"quantity_kg":1}).status_code==422
    assert client.post("/api/v1/inventory",json=inventory(quantity_kg=-1)).status_code==422
    assert client.post("/api/v1/recipients",json=recipient(capacity_kg=0)).status_code==422
