"""add content coloum to posts table

Revision ID: 96dd37d3dd8e
Revises: 0fd6d47e3385
Create Date: 2023-07-24 11:22:00.202378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96dd37d3dd8e'
down_revision = '0fd6d47e3385'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
