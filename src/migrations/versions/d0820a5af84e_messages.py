"""messages

Revision ID: d0820a5af84e
Revises: 646e6f3b3775
Create Date: 2023-05-13 14:22:36.058657

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd0820a5af84e'
down_revision = '646e6f3b3775'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('channel',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('channel_id', sa.Text(), nullable=False),
    sa.Column('participants_id', sa.ARRAY(sa.Integer()), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('raw_bytes', sa.Text(), nullable=True),
    sa.Column('channel_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['channel.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    op.drop_table('channel')
    # ### end Alembic commands ###