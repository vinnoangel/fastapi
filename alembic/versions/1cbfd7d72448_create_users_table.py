"""create users table

Revision ID: 1cbfd7d72448
Revises: dcdf0471edd1
Create Date: 2022-01-10 15:06:22.353488

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.sqltypes import Integer, String


# revision identifiers, used by Alembic.
revision = '1cbfd7d72448'
down_revision = 'dcdf0471edd1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
