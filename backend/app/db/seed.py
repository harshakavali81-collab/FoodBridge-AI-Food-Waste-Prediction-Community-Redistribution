"""Fictional demo partner names — not actual businesses or charities."""
from datetime import datetime, timezone, timedelta
from .models import Inventory, Recipient
def seed_demo(db):
    if db.query(Inventory).first() is not None:
        return
    now = datetime.now(timezone.utc)
    db.add_all([
        Recipient(name="Community Pantry Alpha (Demo)", verified=True, capacity_kg=80, accepts_categories="all", storage_type="ambient", latitude=17.401, longitude=78.469, demo=True),
        Recipient(name="Relief Kitchen Beta (Demo)", verified=True, capacity_kg=65, accepts_categories="produce,grains,bakery", storage_type="chilled", latitude=17.425, longitude=78.448, demo=True),
        Recipient(name="Food Support Gamma (Demo)", verified=True, capacity_kg=120, accepts_categories="all", storage_type="chilled", latitude=17.409, longitude=78.477, demo=True),
        Recipient(name="Neighborhood Aid Delta (Demo)", verified=False, capacity_kg=55, accepts_categories="all", storage_type="ambient", latitude=17.380, longitude=78.490, demo=True),
        Recipient(name="Grain Bank Epsilon (Demo)", verified=True, capacity_kg=100, accepts_categories="grains,bakery,produce", storage_type="ambient", latitude=17.414, longitude=78.455, demo=True),
        Inventory(partner_name="Green Bowl Cafe (Demo)",food_name="Vegetable boxes",category="produce",quantity_kg=42,allocated_kg=0,storage_type="chilled",allergen_info="Check labeling",food_safety_confirmed=True,safety_notes="Synthetic acknowledged food review",expires_at=now+timedelta(hours=25),pickup_by=now+timedelta(hours=10),latitude=17.412,longitude=78.452,demo=True),
        Inventory(partner_name="City Bakery (Demo)",food_name="Bread loaves",category="bakery",quantity_kg=32,allocated_kg=0,storage_type="ambient",allergen_info="Wheat, may contain dairy",food_safety_confirmed=True,safety_notes="Illustrative safety check",expires_at=now+timedelta(hours=34),pickup_by=now+timedelta(hours=20),latitude=17.399,longitude=78.466,demo=True),
        Inventory(partner_name="Harvest Market (Demo)",food_name="Rice and pulse packs",category="grains",quantity_kg=75,allocated_kg=0,storage_type="ambient",allergen_info="Check original pack",food_safety_confirmed=True,safety_notes="Illustrative safety check",expires_at=now+timedelta(days=12),pickup_by=now+timedelta(days=3),latitude=17.408,longitude=78.463,demo=True),
        Inventory(partner_name="FreshFork Kitchen (Demo)",food_name="Prepared meals",category="prepared",quantity_kg=21,allocated_kg=0,storage_type="chilled",allergen_info="Milk, wheat",food_safety_confirmed=False,safety_notes="Requires a manual temperature check",expires_at=now+timedelta(hours=8),pickup_by=now+timedelta(hours=3),latitude=17.421,longitude=78.458,demo=True),
        Inventory(partner_name="Sunrise Grocer (Demo)",food_name="Fruit crates",category="produce",quantity_kg=54,allocated_kg=0,storage_type="ambient",allergen_info="Check labels",food_safety_confirmed=True,safety_notes="Illustrative safety check",expires_at=now+timedelta(hours=42),pickup_by=now+timedelta(hours=24),latitude=17.419,longitude=78.490,demo=True)
    ])
    db.commit()
