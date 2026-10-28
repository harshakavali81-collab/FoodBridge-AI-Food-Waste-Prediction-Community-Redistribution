"""Initial schema on a new, empty synthetic demo database.

Revision ID: 20261028_01
Revises:
Do NOT run on an existing unmanaged database; approve backup and baseline first.
"""
from alembic import op
import sqlalchemy as sa

revision="20261028_01"
down_revision=None
branch_labels=None
depends_on=None

def upgrade():
    op.create_table(
        "inventory",
        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("partner_name",sa.String(120),nullable=False),
        sa.Column("food_name",sa.String(120),nullable=False),
        sa.Column("category",sa.String(60),nullable=False),
        sa.Column("quantity_kg",sa.Float(),nullable=False),
        sa.Column("allocated_kg",sa.Float(),nullable=False),
        sa.Column("storage_type",sa.String(20),nullable=False),
        sa.Column("allergen_info",sa.String(250),nullable=False),
        sa.Column("food_safety_confirmed",sa.Boolean(),nullable=False),
        sa.Column("safety_notes",sa.Text(),nullable=False),
        sa.Column("expires_at",sa.DateTime(timezone=True),nullable=False),
        sa.Column("pickup_by",sa.DateTime(timezone=True),nullable=False),
        sa.Column("latitude",sa.Float(),nullable=False),
        sa.Column("longitude",sa.Float(),nullable=False),
        sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),
        sa.Column("demo",sa.Boolean(),nullable=False),
    )
    op.create_table(
        "recipients",
        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("name",sa.String(120),nullable=False,unique=True),
        sa.Column("verified",sa.Boolean(),nullable=False),
        sa.Column("capacity_kg",sa.Float(),nullable=False),
        sa.Column("accepts_categories",sa.String(200),nullable=False),
        sa.Column("storage_type",sa.String(20),nullable=False),
        sa.Column("latitude",sa.Float(),nullable=False),
        sa.Column("longitude",sa.Float(),nullable=False),
        sa.Column("demo",sa.Boolean(),nullable=False),
    )
    op.create_table(
        "donations",
        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("inventory_id",sa.Integer(),sa.ForeignKey("inventory.id"),nullable=False),
        sa.Column("recipient_id",sa.Integer(),sa.ForeignKey("recipients.id"),nullable=False),
        sa.Column("quantity_kg",sa.Float(),nullable=False),
        sa.Column("status",sa.String(20),nullable=False),
        sa.Column("pickup_confirmed_by",sa.String(120),nullable=True),
        sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),
        sa.Column("collected_at",sa.DateTime(timezone=True),nullable=True),
        sa.Column("demo",sa.Boolean(),nullable=False),
    )
    op.create_table(
        "audit_events",
        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("event_type",sa.String(64),nullable=False),
        sa.Column("entity_type",sa.String(64),nullable=False),
        sa.Column("entity_id",sa.Integer(),nullable=False),
        sa.Column("quantity_kg",sa.Float(),nullable=True),
        sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),
        sa.Column("demo",sa.Boolean(),nullable=False),
    )
    op.create_index("ix_audit_events_event_type","audit_events",["event_type"])

def downgrade():
    # DESTROYS data. Tested only on throwaway synthetic databases.
    op.drop_index("ix_audit_events_event_type",table_name="audit_events")
    op.drop_table("audit_events")
    op.drop_table("donations")
    op.drop_table("recipients")
    op.drop_table("inventory")
