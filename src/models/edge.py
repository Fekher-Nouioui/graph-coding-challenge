"""Edge model representing a directed connection between nodes."""
from sqlalchemy import Column, BigInteger, ForeignKey
from src.models.base import Base


class Edge(Base):
    """Edge entity representing a directed connection in the graph.

    Attributes:
        id: Unique identifier (primary key)
        source_node_id: ID of the source node (from)
        target_node_id: ID of the target node (to)
    """

    __tablename__ = "edges"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    source_node_id = Column(
        BigInteger, ForeignKey("nodes.id", ondelete="CASCADE"), nullable=False
    )
    target_node_id = Column(
        BigInteger, ForeignKey("nodes.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Edge(id={self.id}, {self.source_node_id} -> {self.target_node_id})>"
