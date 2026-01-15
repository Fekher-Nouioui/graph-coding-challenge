"""create nodes and edges tables

Revision ID: 001
Revises:
Create Date: 2026-01-14

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create nodes and edges tables."""
    # Create nodes table
    op.execute(
        """
        CREATE TABLE nodes (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL
        )
        """
    )

    # Create edges table
    op.execute(
        """
        CREATE TABLE edges (
            id BIGINT PRIMARY KEY AUTO_INCREMENT,
            source_node_id BIGINT NOT NULL,
            target_node_id BIGINT NOT NULL,
            FOREIGN KEY (source_node_id) REFERENCES nodes(id) ON DELETE CASCADE,
            FOREIGN KEY (target_node_id) REFERENCES nodes(id) ON DELETE CASCADE
        )
        """
    )


def downgrade() -> None:
    """Drop edges and nodes tables."""
    op.execute("DROP TABLE IF EXISTS edges")
    op.execute("DROP TABLE IF EXISTS nodes")
