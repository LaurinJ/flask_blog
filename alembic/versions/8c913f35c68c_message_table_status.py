"""Message table status

Revision ID: 8c913f35c68c
Revises: 23e2ebc59068
Create Date: 2020-01-14 22:33:01.799956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c913f35c68c'
down_revision = '23e2ebc59068'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("message", sa.Column("status", sa.BOOLEAN, default=True))


def downgrade():
    op.drop_column("message", "status")
