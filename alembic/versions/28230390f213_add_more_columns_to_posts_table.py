"""add more columns to posts table

Revision ID: 28230390f213
Revises: 87c50fc186c6
Create Date: 2022-01-10 15:30:58.748248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28230390f213'
down_revision = '87c50fc186c6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),
    )
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
