"""add performance indexes

Revision ID: 002
Revises: 001
Create Date: 2026-01-14

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add indexes for graph traversal performance."""
    # Index on source_node_id for forward traversal (CRITICAL for recursive CTE)
    op.execute("CREATE INDEX idx_source ON edges(source_node_id)")

    # Index on target_node_id for reverse queries (optional but recommended)
    op.execute("CREATE INDEX idx_target ON edges(target_node_id)")


def downgrade() -> None:
    """Remove performance indexes."""
    op.execute("DROP INDEX idx_target ON edges")
    op.execute("DROP INDEX idx_source ON edges")
