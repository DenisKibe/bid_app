"""empty message

Revision ID: e4f4af039e4e
Revises: 4df17fd4c622
Create Date: 2021-02-20 12:26:49.462580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4f4af039e4e'
down_revision = '4df17fd4c622'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'account_detail', ['id'])
    op.create_unique_constraint(None, 'bid', ['id'])
    op.create_unique_constraint(None, 'outlet', ['id'])
    op.create_unique_constraint(None, 'product', ['id'])
    op.create_unique_constraint(None, 'product_category', ['id'])
    op.create_unique_constraint(None, 'user', ['id'])
    op.create_unique_constraint(None, 'wallet', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'wallet', type_='unique')
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'product_category', type_='unique')
    op.drop_constraint(None, 'product', type_='unique')
    op.drop_constraint(None, 'outlet', type_='unique')
    op.drop_constraint(None, 'bid', type_='unique')
    op.drop_constraint(None, 'account_detail', type_='unique')
    # ### end Alembic commands ###
