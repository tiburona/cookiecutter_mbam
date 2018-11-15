"""empty message

Revision ID: 41c4afae419c
Revises: 
Create Date: 2018-11-15 13:27:00.461536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41c4afae419c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.Binary(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('xnat_subject_id', sa.String(length=80), nullable=True),
    sa.Column('num_experiments', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('experiments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('scanner', sa.String(length=80), nullable=True),
    sa.Column('num_scans', sa.Integer(), nullable=True),
    sa.Column('xnat_experiment_id', sa.String(length=80), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('scan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('xnat_uri', sa.String(length=255), nullable=True),
    sa.Column('experiment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['experiment_id'], ['experiments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scan')
    op.drop_table('roles_users')
    op.drop_table('experiments')
    op.drop_table('users')
    op.drop_table('roles')
    # ### end Alembic commands ###