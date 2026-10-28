from types import SimpleNamespace
from datetime import datetime,timezone,timedelta
from foodbridge.matching.eligibility import eligibility
from foodbridge.matching.route_cost import haversine_km
def pair():
    now=datetime.now(timezone.utc)
    item=SimpleNamespace(food_safety_confirmed=True,expires_at=now+timedelta(days=2),pickup_by=now+timedelta(hours=6),storage_type="chilled",category="produce",quantity_kg=20,allocated_kg=2,latitude=17.4,longitude=78.4)
    r=SimpleNamespace(verified=True,storage_type="chilled",accepts_categories="produce",capacity_kg=12,latitude=17.41,longitude=78.4)
    return item,r
def test_distance():
    assert haversine_km(0,0,0,0)==0
    assert 110<haversine_km(0,0,0,1)<112
def test_quantity_and_radius():
    item,r=pair()
    assert eligibility(item,r)["eligible"]
    assert eligibility(item,r)["max_quantity_kg"]==12
    assert not eligibility(item,r,quantity_kg=13)["eligible"]
    assert not eligibility(item,r,max_distance_km=.1)["eligible"]
def test_no_automatic_food_safety():
    item,r=pair();item.food_safety_confirmed=False;r.verified=False
    reasons=eligibility(item,r)["reasons"]
    assert any("safety" in x.lower() for x in reasons)
    assert any("not verified" in x.lower() for x in reasons)
