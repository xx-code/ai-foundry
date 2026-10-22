"""update user mcp server

Revision ID: 47ee7129130e
Revises: b82c1a6f4e31
Create Date: 2026-10-22 14:36:55.882409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '47ee7129130e'
down_revision: Union[str, Sequence[str], None] = 'b82c1a6f4e31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    server_app_enum = postgresql.ENUM('AGNI_APP', name='mcpclientapp')
    server_app_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        'user_mcp_servers',
        sa.Column('server_app', server_app_enum, nullable=True),
    )
    op.execute(
        "UPDATE user_mcp_servers SET server_app = 'AGNI_APP' "
        "WHERE server_app IS NULL"
    )
    op.alter_column('user_mcp_servers', 'server_app', nullable=False)

    op.add_column(
        'user_mcp_servers',
        sa.Column('client_cred', sa.JSON(), nullable=True),
    )
    op.execute(
        "UPDATE user_mcp_servers "
        "SET client_cred = json_build_object('encrypt_api_key', encrypt_api_key) "
        "WHERE client_cred IS NULL"
    )
    op.alter_column('user_mcp_servers', 'client_cred', nullable=False)

    op.drop_column('user_mcp_servers', 'hostname')
    op.drop_column('user_mcp_servers', 'encrypt_api_key')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('user_mcp_servers', sa.Column('encrypt_api_key', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.add_column('user_mcp_servers', sa.Column('hostname', sa.VARCHAR(length=253), autoincrement=False, nullable=True))
    op.execute(
        "UPDATE user_mcp_servers "
        "SET encrypt_api_key = client_cred ->> 'encrypt_api_key', "
        "hostname = server_app::text"
    )
    op.drop_column('user_mcp_servers', 'client_cred')
    op.drop_column('user_mcp_servers', 'server_app')
    postgresql.ENUM('AGNI_APP', name='mcpclientapp').drop(
        op.get_bind(),
        checkfirst=True,
    )
