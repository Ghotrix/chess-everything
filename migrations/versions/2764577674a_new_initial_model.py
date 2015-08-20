"""New initial model.

Revision ID: 2764577674a
Revises: None
Create Date: 2015-08-09 14:07:03.495084

"""

# revision identifiers, used by Alembic.
revision = '2764577674a'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('moves',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source_position_id', sa.Integer(), nullable=True),
    sa.Column('destination_position_id', sa.Integer(), nullable=True),
    sa.Column('san', sa.String(length=8), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_moves_source_position_id'), 'moves', ['source_position_id'], unique=False)
    op.create_table('positions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fen', sa.String(length=88), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_positions_fen'), 'positions', ['fen'], unique=True)
    op.create_table('quality',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=7), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('user_moves',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('move_id', sa.Integer(), nullable=False),
    sa.Column('quality_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['move_id'], ['moves.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'move_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_moves')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('quality')
    op.drop_index(op.f('ix_positions_fen'), table_name='positions')
    op.drop_table('positions')
    op.drop_index(op.f('ix_moves_source_position_id'), table_name='moves')
    op.drop_table('moves')
    ### end Alembic commands ###