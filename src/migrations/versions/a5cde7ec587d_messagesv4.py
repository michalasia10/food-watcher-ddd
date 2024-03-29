"""messagesv4

Revision ID: a5cde7ec587d
Revises: b0115bad29ec
Create Date: 2023-05-13 16:31:59.568150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5cde7ec587d'
down_revision = 'b0115bad29ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('channel', sa.Column('name', sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('channel', 'name')
    # ### end Alembic commands ###
