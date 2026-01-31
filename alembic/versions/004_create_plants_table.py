"""create plants table

Revision ID: 004
Revises: 003
Create Date: 2026-01-31

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '004'
down_revision: Union[str, None] = '003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create plants table
    op.create_table(
        'plants',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('difficulty_level', sa.String(length=255), nullable=True),
        sa.Column('duration_days', sa.String(length=255), nullable=True),
        sa.Column('recommendations', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('prohibitions', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('image_url', sa.String(length=500), nullable=True),
        sa.Column('requirements', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('unit', sa.String(length=50), nullable=True),
        sa.Column('market_price_per_unit', sa.DECIMAL(precision=12, scale=2), nullable=True),
        sa.Column('growth_phases', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('common_diseases', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plants_id'), 'plants', ['id'], unique=False)
    op.create_index(op.f('ix_plants_category'), 'plants', ['category'], unique=False)
    op.create_index(op.f('ix_plants_name'), 'plants', ['name'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_plants_name'), table_name='plants')
    op.drop_index(op.f('ix_plants_category'), table_name='plants')
    op.drop_index(op.f('ix_plants_id'), table_name='plants')
    op.drop_table('plants')
