"""contact message

Revision ID: a239ae13ce74
Revises: f7c462060fad
Create Date: 2019-12-30 15:53:20.964817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a239ae13ce74'
down_revision = 'f7c462060fad'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("message",
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("first_name", sa.String, nullable=False),
                    sa.Column("last_name", sa.String, nullable=False),
                    sa.Column("email", sa.String, nullable=False),
                    sa.Column("tel_number", sa.Integer, nullable=False),
                    sa.Column("message", sa.String, nullable=False))


def downgrade():
    op.drop_table("message")
