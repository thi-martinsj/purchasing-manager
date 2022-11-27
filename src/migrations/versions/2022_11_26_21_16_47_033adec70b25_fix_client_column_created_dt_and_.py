"""Fix client column created_dt and updated_dt

Revision ID: 033adec70b25
Revises: 5a8b2785d287
Create Date: 2022-11-26 21:16:47.143040

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "033adec70b25"
down_revision = "5a8b2785d287"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("client", "created_dt", existing_type=postgresql.TIMESTAMP(timezone=True), nullable=False)
    op.alter_column("client", "updated_dt", existing_type=postgresql.TIMESTAMP(timezone=True), nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("client", "updated_dt", existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True)
    op.alter_column("client", "created_dt", existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True)
    # ### end Alembic commands ###