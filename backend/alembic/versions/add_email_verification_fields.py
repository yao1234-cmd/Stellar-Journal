"""Add email verification fields to users table

Revision ID: add_email_verification
Revises: 7fe88b5fc215
Create Date: 2026-01-22 21:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_email_verification'
down_revision = '7fe88b5fc215'
branch_labels = None
depends_on = None


def upgrade():
    # Add email verification fields to users table
    op.add_column('users', sa.Column('is_email_verified', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('verification_token', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('verification_token_expires', sa.DateTime(timezone=True), nullable=True))


def downgrade():
    # Remove email verification fields
    op.drop_column('users', 'verification_token_expires')
    op.drop_column('users', 'verification_token')
    op.drop_column('users', 'is_email_verified')
