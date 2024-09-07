"""Add two_factor_secret column to User model

Revision ID: 65d61052cc2e
Revises: 1b4b6738926c
Create Date: 2024-09-07 13:40:50.509511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65d61052cc2e'
down_revision = '1b4b6738926c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        # Add the 'email' column as nullable initially
        batch_op.add_column(sa.Column('email', sa.String(length=50), nullable=True))
        
        # Migrate data here if necessary
        # Optionally populate 'email' column if it's from another column or source
        # Example (replace with actual logic if needed):
        # op.execute("UPDATE user SET email = COALESCE(Email, 'default@example.com')")

        # After populating 'email', make it non-nullable and add the constraint
        batch_op.alter_column('email', nullable=False)
        
        # Add other columns
        batch_op.add_column(sa.Column('two_factor_secret', sa.String(length=32), nullable=True))
        batch_op.create_unique_constraint('uq_user_email', ['email'])
        
        # Drop the old 'Email' column if needed
        batch_op.drop_column('Email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        # Recreate the old 'Email' column if necessary
        batch_op.add_column(sa.Column('Email', sa.VARCHAR(length=50), nullable=False))
        batch_op.drop_constraint('uq_user_email', type_='unique')
        batch_op.drop_column('two_factor_secret')
        batch_op.drop_column('email')

    # ### end Alembic commands ###