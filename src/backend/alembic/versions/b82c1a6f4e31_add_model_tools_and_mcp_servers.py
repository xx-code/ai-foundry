"""add model tools and user mcp servers

Revision ID: b82c1a6f4e31
Revises: 014099fc0a80
Create Date: 2026-10-21

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b82c1a6f4e31"
down_revision: Union[str, Sequence[str], None] = "014099fc0a80"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_mcp_servers",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("hostname", sa.String(length=253), nullable=False),
        sa.Column("encrypt_api_key", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "model_tools",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("model_id", sa.Uuid(), nullable=False),
        sa.Column("tool_id", sa.String(length=100), nullable=False),
        sa.Column(
            "tool_type",
            sa.Enum(
                "WEB_SEARCH",
                "CODE_INTERPRETOR",
                "MCP_SERVER",
                name="aitooltype",
            ),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["model_id"], ["models.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("model_tools")
    op.drop_table("user_mcp_servers")
