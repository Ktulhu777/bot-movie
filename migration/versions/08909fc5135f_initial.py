"""'initial'

Revision ID: 08909fc5135f
Revises: ae6970a10341
Create Date: 2024-07-30 20:04:05.664887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08909fc5135f'
down_revision: Union[str, None] = 'ae6970a10341'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
