"""empty message

Revision ID: c39780eb7def
Revises: None
Create Date: 2016-10-08 18:35:32.696110

"""

# revision identifiers, used by Alembic.
revision = 'c39780eb7def'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('filename', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    ### end Alembic commands ###
