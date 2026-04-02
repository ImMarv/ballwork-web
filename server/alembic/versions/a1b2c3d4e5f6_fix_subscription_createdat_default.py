"""fix subscription createdAt default

Revision ID: a1b2c3d4e5f6
Revises: 286931df51b6
Create Date: 2026-04-02 16:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "286931df51b6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Defensive backfill in case any rows were inserted before the default existed.
    op.execute(
        'UPDATE subscription_digest SET "createdAt" = CURRENT_TIMESTAMP WHERE "createdAt" IS NULL'
    )

    op.alter_column(
        "subscription_digest",
        "createdAt",
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "subscription_digest",
        "createdAt",
        existing_type=sa.DateTime(timezone=True),
        server_default=None,
        existing_nullable=False,
    )
