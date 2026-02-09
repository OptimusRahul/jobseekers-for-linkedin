"""add_user_id_to_hr_contacts

Revision ID: a6bf302e9f4d
Revises: b607e09cf3b3
Create Date: 2026-02-10 01:19:13.895085

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a6bf302e9f4d'
down_revision: Union[str, None] = 'b607e09cf3b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add user_id column as nullable first (to handle existing data)
    op.add_column('hr_contacts', sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True))
    
    # Note: If there are existing hr_contacts, you'll need to populate user_id before making it NOT NULL
    # For now, we'll leave it nullable. If you want to make it NOT NULL:
    # 1. Populate existing rows with a default user_id
    # 2. Run: op.alter_column('hr_contacts', 'user_id', nullable=False)
    
    # Add foreign key constraint
    op.create_foreign_key(
        'fk_hr_contacts_user_id',
        'hr_contacts',
        'users',
        ['user_id'],
        ['id'],
        ondelete='CASCADE'
    )
    
    # Add index on user_id for better query performance
    op.create_index('ix_hr_contacts_user_id', 'hr_contacts', ['user_id'])


def downgrade() -> None:
    # Remove index
    op.drop_index('ix_hr_contacts_user_id', table_name='hr_contacts')
    
    # Remove foreign key constraint
    op.drop_constraint('fk_hr_contacts_user_id', 'hr_contacts', type_='foreignkey')
    
    # Remove user_id column
    op.drop_column('hr_contacts', 'user_id')
