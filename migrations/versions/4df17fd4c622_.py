"""empty message

Revision ID: 4df17fd4c622
Revises: 
Create Date: 2021-02-19 00:39:38.502904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4df17fd4c622'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('outlet',
    sa.Column('id', sa.String(length=20), server_default='Eg782UFbMdco5xPt', autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('product_category',
    sa.Column('id', sa.String(length=20), server_default='5zNBcpWB67Epy7kF', autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.String(length=20), server_default='iKGT4kFeKzPdE8jh', autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('buying_price', sa.Integer(), nullable=False),
    sa.Column('state', sa.String(length=10), nullable=False),
    sa.Column('category_id', sa.String(length=20), nullable=False),
    sa.Column('image_url', sa.String(length=100), nullable=False),
    sa.Column('outlet_id', sa.String(length=20), nullable=False),
    sa.Column('expiry_date', sa.DateTime(), nullable=True),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_on', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['product_category.id'], ),
    sa.ForeignKeyConstraint(['outlet_id'], ['outlet.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.String(length=20), server_default='HrGaKfLLsBqlt5AQ', autoincrement=False, nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('role', sa.String(length=10), server_default='User', nullable=False),
    sa.Column('outlet_id', sa.String(length=20), nullable=False),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_on', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['outlet_id'], ['outlet.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('account_detail',
    sa.Column('id', sa.String(length=20), server_default='5XepfVC7BdMFKmbR', autoincrement=False, nullable=False),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('nickname', sa.String(length=50), nullable=True),
    sa.Column('middle_name', sa.String(length=50), nullable=True),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.Column('id_number', sa.String(length=10), nullable=True),
    sa.Column('dob', sa.DateTime(), nullable=True),
    sa.Column('gender', sa.String(length=10), nullable=True),
    sa.Column('profile_pic_url', sa.String(length=100), nullable=True),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_on', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('is_email_verified', sa.Boolean(), server_default='False', nullable=True),
    sa.Column('is_phone_verified', sa.Boolean(), server_default='False', nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('bid',
    sa.Column('id', sa.String(length=20), server_default='EaqU2364IOg6MGU4', autoincrement=False, nullable=False),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('product_id', sa.String(length=20), nullable=False),
    sa.Column('bid_amount', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_on', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('code',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('code', sa.String(length=6), server_default='0mIFi6', nullable=False),
    sa.Column('field', sa.String(length=100), nullable=False),
    sa.Column('expiry_time', sa.Time(), nullable=True),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wallet',
    sa.Column('id', sa.String(length=20), server_default='cp7VcqkUvx0VYMNm', autoincrement=False, nullable=False),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('balance', sa.Integer(), server_default='0', nullable=True),
    sa.Column('bonus', sa.Integer(), server_default='0', nullable=True),
    sa.Column('updated_on', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wallet')
    op.drop_table('code')
    op.drop_table('bid')
    op.drop_table('account_detail')
    op.drop_table('user')
    op.drop_table('product')
    op.drop_table('product_category')
    op.drop_table('outlet')
    # ### end Alembic commands ###
