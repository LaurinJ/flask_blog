"""User model

Revision ID: 23e2ebc59068
Revises: f9432abeb2ac
Create Date: 2019-12-30 21:09:29.451609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23e2ebc59068'
down_revision = 'f9432abeb2ac'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("user", sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("username", sa.String, nullable=False, unique=True),
                    sa.Column("password", sa.String, nullable=False),
                    sa.Column("email", sa.String, nullable=False),
                    sa.Column("created_at", sa.DateTime, nullable=False),
                    sa.Column("image", sa.String, default="default.jpg"))


def downgrade():
    op.drop_table("user")
