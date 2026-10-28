"""Isolated pilot readiness checklist (fictional-only).

Revision ID: 20261028_02
Revises: 20261028_01
"""
from alembic import op
import sqlalchemy as sa

revision="20261028_02"
down_revision="20261028_01"
branch_labels=None
depends_on=None

def upgrade():
    op.create_table(
        "pilot_reviews",
        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("tenant_id",sa.String(64),nullable=False),
        sa.Column("check_key",sa.String(60),nullable=False),
        sa.Column("status",sa.String(30),nullable=False),
        sa.Column("evidence_ref",sa.String(85),nullable=False),
        sa.Column("reviewed_by",sa.String(128),nullable=False),
        sa.Column("reviewed_at",sa.DateTime(timezone=True),nullable=False),
        sa.UniqueConstraint("tenant_id","check_key",name="uq_pilot_review_tenant_check"),
    )
    op.create_index("ix_pilot_reviews_tenant_id","pilot_reviews",["tenant_id"])

def downgrade():
    op.drop_index("ix_pilot_reviews_tenant_id",table_name="pilot_reviews")
    op.drop_table("pilot_reviews")
