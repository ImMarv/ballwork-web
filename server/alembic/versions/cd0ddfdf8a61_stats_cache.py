"""stats_cache

Revision ID: cd0ddfdf8a61
Revises: a1b2c3d4e5f6
Create Date: 2026-04-08 11:46:48.098390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd0ddfdf8a61'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "entity_cache",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cache_key", sa.String(length=64), nullable=False),
        sa.Column("entity_type", sa.String(length=32), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("payload", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_entity_cache_cache_key"),
        "entity_cache",
        ["cache_key"],
        unique=True,
    )
    op.create_index(
        op.f("ix_entity_cache_expires_at"),
        "entity_cache",
        ["expires_at"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_entity_cache_expires_at"), table_name="entity_cache")
    op.drop_index(op.f("ix_entity_cache_cache_key"), table_name="entity_cache")
    op.drop_table("entity_cache")
    # ### end Alembic commands ###
