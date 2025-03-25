"""Fix pdf_data column type

Revision ID: bcb504f40e1f
Revises: f092c0ab42d4  # <-- Change this to match your actual previous revision ID
Create Date: 2025-03-21 23:59:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcb504f40e1f'
down_revision = 'f092c0ab42d4'  # <-- Make sure this matches the last successful revision
branch_labels = None
depends_on = None


def upgrade():
    # Manually alter column using a raw SQL statement with casting
    op.execute("""
        ALTER TABLE fax_files
        ALTER COLUMN pdf_data
        TYPE BYTEA
        USING pdf_data::BYTEA;
    """)


def downgrade():
    # Optional: convert BYTEA back to TEXT using UTF-8 interpretation
    op.execute("""
        ALTER TABLE fax_files
        ALTER COLUMN pdf_data
        TYPE TEXT
        USING convert_from(pdf_data, 'UTF8');
    """)