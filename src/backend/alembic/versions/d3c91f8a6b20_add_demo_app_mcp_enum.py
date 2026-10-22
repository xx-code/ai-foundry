"""add demo app to MCP app enum

Revision ID: d3c91f8a6b20
Revises: 722a87b5ac9d
Create Date: 2026-10-22

"""
from typing import Sequence, Union

from alembic import op


revision: str = "d3c91f8a6b20"
down_revision: Union[str, Sequence[str], None] = "722a87b5ac9d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE mcpclientapp ADD VALUE IF NOT EXISTS 'DEMO_APP'")


def downgrade() -> None:
    # PostgreSQL does not safely support removing an enum value.
    pass