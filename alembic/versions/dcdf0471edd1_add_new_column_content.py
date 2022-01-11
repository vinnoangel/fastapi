"""add new column - content

Revision ID: dcdf0471edd1
Revises: 458b1d47b8f7
Create Date: 2022-01-10 14:46:55.266336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcdf0471edd1'
down_revision = '458b1d47b8f7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
