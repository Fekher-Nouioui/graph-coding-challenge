"""API routes for node operations."""
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from typing import List
import time

from src.database import get_db
from src.services import node_service
from src.schemas.node import NodeResponse, ConnectedNodesResponse

router = APIRouter(prefix="/nodes", tags=["Nodes"])


@router.get("/graph", response_class=Response)
def get_graph_visualization(db: Session = Depends(get_db)):
    """
    Get a text-based visualization of the entire graph.

    This endpoint fetches all nodes and edges from the database and returns
    a simple text representation showing the graph structure.
    """
    graph_text = node_service.get_graph_visualization(db)
    return Response(content=graph_text, media_type="text/plain")

@router.get("/", response_model=List[NodeResponse])
def get_all_nodes(db: Session = Depends(get_db)):
    """Get all nodes"""

    nodes = node_service.get_all_nodes(db)
    return nodes

@router.get(
    "/{node_id}",
    response_model=NodeResponse,
    responses={
        404: {
            "description": "Node not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Node with id not found"}
                }
            }
        },
    }
)
def get_node(node_id: int, db: Session = Depends(get_db)):
    """Get a single node by ID."""

    node = node_service.get_node_by_id(db, node_id)
    if not node:
        raise HTTPException(
            status_code=404, detail=f"Node with id {node_id} not found"
        )
    return node

@router.get(
    "/by-name/{node_name}",
    response_model=NodeResponse,
    responses={
        404: {
            "description": "Node not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Node with name not found"}
                }
            }
        },
    }
)
def get_node_by_name(node_name: str, db: Session = Depends(get_db)):
    """Get a single node by name."""

    node = node_service.get_node_by_name(db, node_name)
    if not node:
        raise HTTPException(
            status_code=404, detail=f"Node with name '{node_name}' not found"
        )
    return node

@router.get(
    "/{node_id}/connected-cte",
    response_model=ConnectedNodesResponse,
    responses={
        404: {
            "description": "Node not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Node with id not found"}
                }
            }
        },
    }
)
def get_connected_nodes_cte(node_id: int, db: Session = Depends(get_db)):
    """Get all nodes reachable from the given node using Recursive CTE."""

    # Start timing from request arrival
    start_time = time.perf_counter()

    # Verify node exists
    node = node_service.get_node_by_id(db, node_id)
    if not node:
        raise HTTPException(
            status_code=404, detail=f"Node with id {node_id} not found"
        )

    # Get connected nodes using recursive CTE
    result = node_service.get_connected_nodes(db, node_id)

    # Calculate total execution time
    end_time = time.perf_counter()
    execution_time_ms = (end_time - start_time) * 1000

    
    return ConnectedNodesResponse(
        source_node_id=result["source_node_id"],
        connected_node_ids=result["connected_node_ids"],
        total_count=result["total_count"],
        execution_time_ms=round(execution_time_ms, 2),
    )

@router.get(
    "/by-name/{node_name}/connected-cte",
    response_model=ConnectedNodesResponse,
    responses={
        404: {
            "description": "Node not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Node with name 'A' not found"}
                }
            }
        },
    }
)
def get_connected_nodes_cte_by_name(node_name: str, db: Session = Depends(get_db)):
    """Get all nodes reachable from the given node using Recursive CTE by the node name"""

    # Start timing from request arrival
    start_time = time.perf_counter()

    # Verify node exists and get its ID
    node = node_service.get_node_by_name(db, node_name)
    if not node:
        raise HTTPException(
            status_code=404, detail=f"Node with name '{node_name}' not found"
        )

    # Get connected nodes using recursive CTE
    result = node_service.get_connected_nodes(db, node.id)

    # Calculate total execution time
    end_time = time.perf_counter()
    execution_time_ms = (end_time - start_time) * 1000

    
    return ConnectedNodesResponse(
        source_node_id=result["source_node_id"],
        connected_node_ids=result["connected_node_ids"],
        total_count=result["total_count"],
        execution_time_ms=round(execution_time_ms, 2),
    )

@router.get(
    "/{node_id}/connected-dfs",
    response_model=ConnectedNodesResponse,
    responses={
        404: {
            "description": "Node not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Node with id not found"}
                }
            }
        },
    }
)
def get_connected_nodes_dfs(node_id: int, db: Session = Depends(get_db)):
    """Get all nodes reachable from the given node by fetching all edges + Python DFS."""

    # Start timing from request arrival
    start_time = time.perf_counter()

    # Verify node exists
    node = node_service.get_node_by_id(db, node_id)
    if not node:
        raise HTTPException(
            status_code=404, detail=f"Node with id {node_id} not found"
        )

    # Get connected nodes using DFS approach
    result = node_service.get_connected_nodes_dfs(db, node_id)

    # Calculate total execution time
    end_time = time.perf_counter()
    execution_time_ms = (end_time - start_time) * 1000

    
    return ConnectedNodesResponse(
        source_node_id=result["source_node_id"],
        connected_node_ids=result["connected_node_ids"],
        total_count=result["total_count"],
        execution_time_ms=round(execution_time_ms, 2),
    )

@router.get(
    "/by-name/{node_name}/connected-dfs",
    response_model=ConnectedNodesResponse,
    responses={
        404: {
            "description": "Node not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Node with name 'A' not found"}
                }
            }
        },
    }
)
def get_connected_nodes_dfs_by_name(node_name: str, db: Session = Depends(get_db)):
    """Get all nodes reachable from the given node by fetching all edges + Python DFS using the node name"""

    # Start timing from request arrival
    start_time = time.perf_counter()

    # Verify node exists and get its ID
    node = node_service.get_node_by_name(db, node_name)
    if not node:
        raise HTTPException(
            status_code=404, detail=f"Node with name '{node_name}' not found"
        )

    # Get connected nodes using DFS approach
    result = node_service.get_connected_nodes_dfs(db, node.id)

    # Calculate total execution time
    end_time = time.perf_counter()
    execution_time_ms = (end_time - start_time) * 1000

    
    return ConnectedNodesResponse(
        source_node_id=result["source_node_id"],
        connected_node_ids=result["connected_node_ids"],
        total_count=result["total_count"],
        execution_time_ms=round(execution_time_ms, 2),
    )





