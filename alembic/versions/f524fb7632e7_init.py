"""init

Revision ID: f524fb7632e7
Revises: 
Create Date: 2024-09-26 12:20:03.305356

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f524fb7632e7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('genre', sa.String(), nullable=True),
    sa.Column('director', sa.String(), nullable=True),
    sa.Column('release_year', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_movies_director'), 'movies', ['director'], unique=False)
    op.create_index(op.f('ix_movies_genre'), 'movies', ['genre'], unique=False)
    op.create_index(op.f('ix_movies_id'), 'movies', ['id'], unique=False)
    op.create_index(op.f('ix_movies_title'), 'movies', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_movies_title'), table_name='movies')
    op.drop_index(op.f('ix_movies_id'), table_name='movies')
    op.drop_index(op.f('ix_movies_genre'), table_name='movies')
    op.drop_index(op.f('ix_movies_director'), table_name='movies')
    op.drop_table('movies')
    # ### end Alembic commands ###
