"""create garden_designs table

Revision ID: 003
Revises: 002
Create Date: 2026-01-31

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create garden_designs table
    op.create_table(
        'garden_designs',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('input_photo_url', sa.String(length=500), nullable=False),
        sa.Column('preferences', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('design_output', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_implemented', sa.Boolean(), default=False, nullable=True),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range')
    )
    op.create_index(op.f('ix_garden_designs_id'), 'garden_designs', ['id'], unique=False)
    op.create_index('ix_garden_designs_user', 'garden_designs', ['user_id', sa.text('created_at DESC')], unique=False)


def downgrade() -> None:
    op.drop_index('ix_garden_designs_user', table_name='garden_designs')
    op.drop_index(op.f('ix_garden_designs_id'), table_name='garden_designs')
    op.drop_table('garden_designs')
