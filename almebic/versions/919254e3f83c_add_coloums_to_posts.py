"""add coloums to posts

Revision ID: 919254e3f83c
Revises: a8d354326305
Create Date: 2023-07-24 11:43:11.792704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '919254e3f83c'
down_revision = 'a8d354326305'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
