"""empty message

Revision ID: 857ce9118298
Revises: 
Create Date: 2024-07-18 17:09:44.170599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '857ce9118298'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_pic', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('profile_pic')

    # ### end Alembic commands ###
