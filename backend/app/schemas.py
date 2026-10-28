from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator
Storage = Literal["ambient","chilled","frozen"]
class InventoryCreate(BaseModel):
    partner_name: str = Field(min_length=2,max_length=120)
    food_name: str = Field(min_length=2,max_length=120)
    category: str = Field(min_length=2,max_length=60)
    quantity_kg: float = Field(gt=0,le=100000)
    storage_type: Storage
    allergen_info: str = Field(min_length=2,max_length=250)
    food_safety_confirmed: bool = False
    safety_notes: str = Field(default="",max_length=3000)
    expires_at: datetime
    pickup_by: datetime
    latitude: float = Field(ge=-90,le=90)
    longitude: float = Field(ge=-180,le=180)
    @model_validator(mode="after")
    def validate_dates(self):
        if self.pickup_by > self.expires_at:
            raise ValueError("Pickup deadline must be before expiry")
        if self.expires_at.tzinfo is None or self.pickup_by.tzinfo is None:
            raise ValueError("Both dates must include a UTC offset")
        return self
class InventoryOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int
    partner_name:str
    food_name:str
    category:str
    quantity_kg:float
    allocated_kg:float
    storage_type:Storage
    allergen_info:str
    food_safety_confirmed:bool
    safety_notes:str
    expires_at:datetime
    pickup_by:datetime
    latitude:float
    longitude:float
    created_at:datetime
    demo:bool
class RecipientCreate(BaseModel):
    name:str=Field(min_length=2,max_length=120)
    verified:bool=False
    capacity_kg:float=Field(gt=0)
    accepts_categories:str="all"
    storage_type:Storage
    latitude:float=Field(ge=-90,le=90)
    longitude:float=Field(ge=-180,le=180)
class RecipientOut(RecipientCreate):
    model_config=ConfigDict(from_attributes=True)
    id:int
    demo:bool
class DonationCreate(BaseModel):
    inventory_id:int
    recipient_id:int
    quantity_kg:float=Field(gt=0)
class DonationOut(DonationCreate):
    model_config=ConfigDict(from_attributes=True)
    id:int
    status:str
    pickup_confirmed_by:str|None
    created_at:datetime
    collected_at:datetime|None
    demo:bool
class ConfirmPickup(BaseModel):
    confirmed_by:str=Field(min_length=2,max_length=120)
