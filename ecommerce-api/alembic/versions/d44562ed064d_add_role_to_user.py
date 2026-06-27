"""add role to user
Revision ID: d44562ed064d
Revises: 98e3ec542093
Create Date: 2026-06-27 23:37:28.660274
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'd44562ed064d'
down_revision: Union[str, Sequence[str], None] = '98e3ec542093'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    userrole = sa.Enum('USER', 'ADMIN', name='userrole')
    userrole.create(op.get_bind())
    op.add_column('user', sa.Column('role', userrole, nullable=False, server_default='USER'))

def downgrade() -> None:
    op.drop_column('user', 'role')
    op.execute('DROP TYPE userrole')
