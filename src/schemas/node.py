"""Pydantic schemas (DTOs) for Node-related API operations."""
from pydantic import BaseModel, Field
from typing import List


class NodeBase(BaseModel):
    """Base schema with shared node attributes."""

    name: str = Field(..., min_length=1, max_length=255, description="Node name/label")


class NodeResponse(NodeBase):
    """Schema for node responses (DTO for GET responses).

    Includes the auto-generated ID from the database.
    """

    id: int = Field(..., description="Unique node identifier")

    class Config:
        """Pydantic configuration."""

        from_attributes = True  # Allows conversion from SQLAlchemy model


class ConnectedNodesResponse(BaseModel):
    """Response schema for the /nodes/{id}/connected endpoint.

    Returns all nodes reachable from a given starting node.
    """

    source_node_id: int = Field(..., description="ID of the starting node")
    connected_node_ids: List[int] = Field(
        ..., description="List of all reachable node IDs"
    )
    total_count: int = Field(..., description="Total number of connected nodes")
    execution_time_ms: float = Field(
        ..., description="Query execution time in milliseconds"
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "source_node_id": 1,
                "connected_node_ids": [2, 3, 4, 5, 6],
                "total_count": 5,
                "execution_time_ms": 2.45,
            }
        }
