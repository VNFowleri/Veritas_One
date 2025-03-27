from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd04f4e6d9b72'
down_revision = 'b1a0a91a4618'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'notes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('patient_id', sa.Integer(), nullable=False),
        sa.Column('note_text', sa.Text(), nullable=False),
        sa.Column('note_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('source_fax_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id']),
        sa.ForeignKeyConstraint(['source_fax_id'], ['fax_files.id']),
    )
    op.create_index('ix_notes_id', 'notes', ['id'], unique=False)

    op.create_table(
        'imaging',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('patient_id', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('date_of_study', sa.DateTime(timezone=True), nullable=True),
        sa.Column('source_fax_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id']),
        sa.ForeignKeyConstraint(['source_fax_id'], ['fax_files.id']),
    )
    op.create_index('ix_imaging_id', 'imaging', ['id'], unique=False)

def downgrade():
    op.drop_table('imaging')
    op.drop_table('notes')