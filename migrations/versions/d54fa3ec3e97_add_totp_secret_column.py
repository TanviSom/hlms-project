"""Add TOTP secret column

Revision ID: d54fa3ec3e97
Revises: 65d61052cc2e
Create Date: 2024-09-07 14:03:48.757540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd54fa3ec3e97'
down_revision = '65d61052cc2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_user')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('totp_secret', sa.String(length=16), nullable=True))
        batch_op.create_unique_constraint(None, ['email'])
        batch_op.drop_column('Email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Email', sa.VARCHAR(length=50), nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('totp_secret')
        batch_op.drop_column('email')

    op.create_table('_alembic_tmp_user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=150), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('phone_number', sa.VARCHAR(length=20), nullable=True),
    sa.Column('email', sa.VARCHAR(length=50), nullable=False),
    sa.Column('two_factor_secret', sa.VARCHAR(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email', name='uq_user_email')
    )
    # ### end Alembic commands ###