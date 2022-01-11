"""add foriegn key to posts table

Revision ID: 87c50fc186c6
Revises: 1cbfd7d72448
Create Date: 2022-01-10 15:23:32.285759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87c50fc186c6'
down_revision = '1cbfd7d72448'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_user_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
