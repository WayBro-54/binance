"""first

Revision ID: 06738b0b4aa9
Revises: 
Create Date: 2023-03-18 17:16:15.658649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06738b0b4aa9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('info_ethusdt',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=True),
    sa.Column('price', sa.DECIMAL(precision=4, scale=8), nullable=True),
    sa.Column('quantity', sa.DECIMAL(precision=4, scale=8), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('info_ethusdt')
    # ### end Alembic commands ###
