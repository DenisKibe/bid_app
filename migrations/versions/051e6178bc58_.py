"""empty message

Revision ID: 051e6178bc58
Revises: e4f4af039e4e
Create Date: 2021-04-01 13:49:31.340450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '051e6178bc58'
down_revision = 'e4f4af039e4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('code', sa.Column('expiry_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('code', 'expiry_time')
    # ### end Alembic commands ###
