"""baseline

Revision ID: c08d25e66237
Revises: 
Create Date: 2022-11-03 21:14:43.177474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c08d25e66237'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('User',
                    sa.Column('idUser', sa.Integer(), nullable=False),
                    sa.Column('username', sa.VARCHAR(length=25), nullable=False),
                    sa.Column('password', sa.VARCHAR(length=15), nullable=False),
                    sa.Column('email', sa.VARCHAR(length=35), nullable=False),
                    sa.Column('firstName', sa.VARCHAR(length=25), nullable=False),
                    sa.Column('lastName', sa.VARCHAR(length=25), nullable=False),
                    sa.Column('userStatus', sa.VARCHAR(length=5), nullable=False),
                    sa.PrimaryKeyConstraint('idUser')
                    )
    op.create_table('Tag',
                    sa.Column('idTag', sa.Integer(), nullable=False),
                    sa.Column('text', sa.VARCHAR(45), nullable=False),
                    sa.PrimaryKeyConstraint('idTag')
                    )
    op.create_table('Note',
                    sa.Column('idNote', sa.Integer(), nullable=False),
                    sa.Column('ownerId', sa.Integer(), nullable=False),
                    sa.Column('title', sa.VARCHAR(45), nullable=False),
                    sa.Column('isPublic', sa.VARCHAR(5), nullable=False),
                    sa.Column('text', sa.VARCHAR(404), nullable=False),
                    sa.Column('dateOfEditing', sa.DateTime, nullable=False),
                    sa.ForeignKeyConstraint(['ownerId'], ['User.idUser']),
                    sa.PrimaryKeyConstraint('idNote')
                    )
    op.create_table('EditNote',
                    sa.Column('idUser', sa.Integer(), nullable=False),
                    sa.Column('idNote', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['idUser'], ['User.idUser']),
                    sa.ForeignKeyConstraint(['idNote'], ['Note.idNote']),
                    sa.PrimaryKeyConstraint('idUser'),
                    sa.PrimaryKeyConstraint('idNote')
                    )
    op.create_table('Tags',
                    sa.Column('idNote', sa.Integer(), nullable=False),
                    sa.Column('idTag', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['idNote'], ['Note.idNote']),
                    sa.ForeignKeyConstraint(['idTag'], ['Tag.idTag']),
                    sa.PrimaryKeyConstraint('idTag'),
                    sa.PrimaryKeyConstraint('idNote')
                    )
    op.create_table('Stats',
                    sa.Column('idStats', sa.Integer(), nullable=False),
                    sa.Column('userId', sa.Integer(), nullable=False),
                    sa.Column('numOfNotes', sa.Integer(), nullable=False),
                    sa.Column('numOfEditingNotes', sa.Integer(), nullable=False),
                    sa.Column('dateOfCreating', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['userId'], ['User.idUser']),
                    sa.PrimaryKeyConstraint('idStats')
                    )
def downgrade():

    op.drop_table('User')
    op.drop_table('Tag')
    op.drop_table('Note')
    op.drop_table('Stats')
    op.drop_table('EditNote')
    op.drop_table('Tags')
