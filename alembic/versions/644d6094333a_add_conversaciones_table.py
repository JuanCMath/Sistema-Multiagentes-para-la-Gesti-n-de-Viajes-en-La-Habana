"""add conversaciones table

Revision ID: 644d6094333a
Revises: df99f31098bf
Create Date: 2025-05-21 22:34:19.912743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '644d6094333a'
down_revision: Union[str, None] = 'df99f31098bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'conversaciones',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('timestamp', sa.DateTime, nullable=False),
        sa.Column('user_id', sa.String, nullable=False),
        sa.Column('pregunta', sa.Text, nullable=False),
        sa.Column('respuesta', sa.Text, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('conversaciones')
