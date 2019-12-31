"""contact message add sending time 

Revision ID: f9432abeb2ac
Revises: a239ae13ce74
Create Date: 2019-12-30 16:23:00.068382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9432abeb2ac'
down_revision = 'a239ae13ce74'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("message", sa.Column("sending_time", sa.DateTime))


def downgrade():
    op.drop_column("message", "sending_time")
