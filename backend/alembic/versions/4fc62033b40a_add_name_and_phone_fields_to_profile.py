"""Add name and phone fields to profile

Revision ID: 4fc62033b40a
Revises: 9afe6855f2c0
Create Date: 2025-07-28 23:45:34.287183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4fc62033b40a'
down_revision: Union[str, None] = '9afe6855f2c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add name and phone columns to profiles table
    op.add_column('profiles', sa.Column('name', sa.String(length=100), nullable=True))
    op.add_column('profiles', sa.Column('phone', sa.String(length=20), nullable=True))


def downgrade() -> None:
    # Remove name and phone columns from profiles table
    op.drop_column('profiles', 'phone')
    op.drop_column('profiles', 'name')
