"""newsleter

Revision ID: f7c462060fad
Revises: 
Create Date: 2019-12-30 14:32:53.114583

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7c462060fad'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("newletter", sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("email", sa.String, nullable=False))


def downgrade():
    op.drop_table("newletter")
