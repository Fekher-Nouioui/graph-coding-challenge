"""Node model representing a vertex in the directed graph."""
from sqlalchemy import Column, BigInteger, String
from src.models.base import Base


class Node(Base):
    """Node entity in the graph database.

    Attributes:
        id: Unique identifier (primary key)
        name: Node name/label
    """

    __tablename__ = "nodes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<Node(id={self.id}, name='{self.name}')>"
