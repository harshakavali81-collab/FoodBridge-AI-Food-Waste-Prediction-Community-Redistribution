"""Demo operational entities. Published FAO research is never used as inventory."""
from datetime import datetime, timezone
from sqlalchemy import Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
def utcnow():
    return datetime.now(timezone.utc)
class Inventory(Base):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    partner_name: Mapped[str] = mapped_column(String(120))
    food_name: Mapped[str] = mapped_column(String(120))
    category: Mapped[str] = mapped_column(String(60))
    quantity_kg: Mapped[float] = mapped_column(Float)
    allocated_kg: Mapped[float] = mapped_column(Float, default=0.)
    storage_type: Mapped[str] = mapped_column(String(20), default="ambient")
    allergen_info: Mapped[str] = mapped_column(String(250), default="Not provided")
    food_safety_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    safety_notes: Mapped[str] = mapped_column(Text, default="")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    pickup_by: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    demo: Mapped[bool] = mapped_column(Boolean, default=False)
class Recipient(Base):
    __tablename__ = "recipients"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    capacity_kg: Mapped[float] = mapped_column(Float)
    accepts_categories: Mapped[str] = mapped_column(String(200), default="all")
    storage_type: Mapped[str] = mapped_column(String(20), default="ambient")
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    demo: Mapped[bool] = mapped_column(Boolean, default=False)
class Donation(Base):
    __tablename__ = "donations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inventory_id: Mapped[int] = mapped_column(ForeignKey("inventory.id"))
    recipient_id: Mapped[int] = mapped_column(ForeignKey("recipients.id"))
    quantity_kg: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(20), default="reserved")
    pickup_confirmed_by: Mapped[str | None] = mapped_column(String(120), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    collected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    demo: Mapped[bool] = mapped_column(Boolean, default=False)

class AuditEvent(Base):
    """Development event summary, not an immutable signed compliance record."""
    __tablename__ = "audit_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_type: Mapped[str] = mapped_column(String(64), index=True)
    entity_type: Mapped[str] = mapped_column(String(64))
    entity_id: Mapped[int] = mapped_column(Integer)
    quantity_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    demo: Mapped[bool] = mapped_column(Boolean, default=True)
