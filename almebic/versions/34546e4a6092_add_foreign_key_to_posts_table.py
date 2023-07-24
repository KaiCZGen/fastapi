"""add foreign key to posts table

Revision ID: 34546e4a6092
Revises: 3c6f04d5c8ac
Create Date: 2023-07-24 11:25:27.779025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34546e4a6092'
down_revision = '3c6f04d5c8ac'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
