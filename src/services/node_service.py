"""Business logic for node operations and graph traversal."""
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import time
from src.models.node import Node
from src.schemas.node import ConnectedNodesResponse


def get_connected_nodes(db: Session, node_id: int) -> dict:
    """Get all nodes reachable from the given node using a recursive CTE query.

    This function implements the core challenge requirement: retrieve all
    connected nodes using a SINGLE database query with MySQL's recursive CTE.

    The query performs a depth-first traversal following directed edges from
    the source node, handling cycles automatically with UNION DISTINCT.

    Args:
        db: SQLAlchemy database session
        node_id: ID of the starting node

    Returns:
        Dictionary with source node ID, list of reachable node IDs,
        and total count (timing will be added at the route handler level)

    Technical Details:
        - Uses MySQL 8.0+ WITH RECURSIVE syntax
        - Base case: Direct children (target_node_id) of source_node_id
        - Recursive case: Children of already discovered nodes
        - UNION DISTINCT prevents infinite loops in cyclic graphs
        - Depth limit of 100 as safety measure
        - Indexed on source_node_id for optimal performance (idx_source)

    Example:
        Given graph: 1 -> 2 -> 3, 1 -> 4
        get_connected_nodes(db, 1) returns [2, 3, 4]
    """
    query = text(
        """
        WITH RECURSIVE reachable_nodes AS (
            -- Base case: Direct children of the starting node
            SELECT target_node_id AS node_id, 1 as depth
            FROM edges
            WHERE source_node_id = :node_id

            UNION DISTINCT

            -- Recursive case: Children of already discovered nodes
            SELECT e.target_node_id, rn.depth + 1
            FROM edges e
            INNER JOIN reachable_nodes rn ON e.source_node_id = rn.node_id
            WHERE rn.depth < 100  -- Safety limit to prevent infinite recursion
        )
        SELECT DISTINCT node_id
        FROM reachable_nodes
        ORDER BY node_id
        """
    )

    result = db.execute(query, {"node_id": node_id})
    connected_ids = [row[0] for row in result]

    return {
        "source_node_id": node_id,
        "connected_node_ids": connected_ids,
        "total_count": len(connected_ids),
    }


def get_node_by_id(db: Session, node_id: int) -> Node | None:
    """Retrieve a single node by its ID.

    Args:
        db: SQLAlchemy database session
        node_id: ID of the node to retrieve

    Returns:
        Node object if found, None otherwise
    """
    return db.query(Node).filter(Node.id == node_id).first()


def get_node_by_name(db: Session, node_name: str) -> Node | None:
    """Retrieve a single node by its name.

    Args:
        db: SQLAlchemy database session
        node_name: Name of the node to retrieve

    Returns:
        Node object if found, None otherwise
    """
    return db.query(Node).filter(Node.name == node_name).first()


def get_all_nodes(db: Session) -> List[Node]:
    """Retrieve all nodes from the database.

    Args:
        db: SQLAlchemy database session

    Returns:
        List of all Node objects ordered by ID
    """
    return db.query(Node).order_by(Node.id).all()


def get_graph_visualization(db: Session) -> str:
    """Generate a simple graph visualization using indented notation.

    Fetches all nodes and edges from the database and creates a clear
    text representation showing parent-child relationships.

    Args:
        db: SQLAlchemy database session

    Returns:
        String containing the graph visualization

    Example output:
        ```
        Graph Visualization
        ===================

        1
          ├─ 2
          │  └─ 4
          └─ 3
             └─ 5

        Isolated nodes: 6, 7
        ```
    """
    from src.models.edge import Edge

    # Fetch all nodes and edges
    all_nodes = db.query(Node).order_by(Node.id).all()
    all_edges = db.query(Edge).order_by(Edge.source_node_id, Edge.target_node_id).all()

    # Build adjacency list (graph structure)
    graph = {}
    children_set = set()
    for edge in all_edges:
        if edge.source_node_id not in graph:
            graph[edge.source_node_id] = []
        graph[edge.source_node_id].append(edge.target_node_id)
        children_set.add(edge.target_node_id)

    # Find root nodes (nodes that are not children of any other node)
    all_node_ids = set(node.id for node in all_nodes)
    root_nodes = sorted(all_node_ids - children_set)

    # Find isolated nodes (no incoming or outgoing edges)
    nodes_with_edges = set(graph.keys()) | children_set
    isolated_nodes = sorted(all_node_ids - nodes_with_edges)

    lines = []
    lines.append("Graph Visualization")
    lines.append("=" * 60)
    lines.append("")

    # Draw each root node as a separate tree
    for root_id in root_nodes:
        tree_lines = _draw_indented_tree(root_id, graph, set(), "", True)
        lines.extend(tree_lines)
        lines.append("")

    # Show isolated nodes
    if isolated_nodes:
        isolated_str = ", ".join(str(node_id) for node_id in isolated_nodes)
        lines.append(f"Isolated nodes: {isolated_str}")
        lines.append("")

    lines.append("=" * 60)
    lines.append(f"Total nodes: {len(all_nodes)} | Total edges: {len(all_edges)}")

    return "\n".join(lines)


def _draw_indented_tree(
    node_id: int, graph: dict, visited: set, prefix: str, is_last: bool
) -> list:
    """Draw an indented tree representation.

    Args:
        node_id: Current node to draw
        graph: Adjacency list representation
        visited: Set of already visited nodes (to prevent cycles)
        prefix: String prefix for current line (for indentation)
        is_last: Whether this is the last child of its parent

    Returns:
        List of strings representing the tree lines
    """
    lines = []

    # Check for cycles
    if node_id in visited:
        lines.append(f"{node_id} [CYCLE]")
        return lines

    visited.add(node_id)

    # Draw the node
    lines.append(str(node_id))

    # Get children
    children = graph.get(node_id, [])

    for i, child_id in enumerate(children):
        is_last_child = i == len(children) - 1

        # Connector for this child
        if is_last_child:
            lines.append(prefix + "  └─ " + str(child_id))
            extension = prefix + "     "
        else:
            lines.append(prefix + "  ├─ " + str(child_id))
            extension = prefix + "  │  "

        # Get grandchildren
        grandchildren = graph.get(child_id, [])
        if grandchildren:
            for j, grandchild_id in enumerate(grandchildren):
                is_last_grandchild = j == len(grandchildren) - 1
                grandchild_lines = _draw_indented_tree(
                    grandchild_id, graph, visited, extension, is_last_grandchild
                )
                # Add connector
                if is_last_grandchild:
                    lines.append(extension + "└─ " + grandchild_lines[0])
                    new_prefix = extension + "   "
                else:
                    lines.append(extension + "├─ " + grandchild_lines[0])
                    new_prefix = extension + "│  "

                # Add rest of the tree
                for line in grandchild_lines[1:]:
                    lines.append(new_prefix + line)

    return lines


def _draw_classic_tree(
    node_id: int, graph: dict, node_map: dict, visited: set, indent: int = 0
) -> list:
    """Draw a classic ASCII tree with slashes and pipes.

    Args:
        node_id: Current node to draw
        graph: Adjacency list representation
        node_map: Map of node_id -> node_name (not used, kept for compatibility)
        visited: Set of already visited nodes (to prevent cycles)
        indent: Current indentation level

    Returns:
        List of strings representing the tree lines
    """
    lines = []

    # Check for cycles
    if node_id in visited:
        lines.append(" " * indent + f"{node_id} [CYCLE]")
        return lines

    visited.add(node_id)

    # Draw the node (ID only)
    lines.append(" " * indent + str(node_id))

    # Get children
    children = graph.get(node_id, [])

    if not children:
        return lines

    # If only one child, use a pipe |
    if len(children) == 1:
        lines.append(" " * indent + "|")
        child_lines = _draw_classic_tree(children[0], graph, node_map, visited, indent)
        lines.extend(child_lines)
    else:
        # Multiple children: draw branches with / and \
        num_children = len(children)

        # Draw the branch lines
        branch_line = " " * indent
        for i in range(num_children):
            if i == 0:
                branch_line += "/"
            elif i == num_children - 1:
                branch_line += "\\"
            else:
                branch_line += " "
            if i < num_children - 1:
                branch_line += " " * 7  # Fixed spacing between branches

        lines.append(branch_line)

        # Draw children nodes on the same line
        children_line = " " * indent
        for i, child_id in enumerate(children):
            child_text = str(child_id)
            if i == 0:
                children_line += child_text
            else:
                # Calculate spacing to align with the branch
                spacing_needed = (indent + i * 8) - len(children_line)
                children_line += " " * spacing_needed + child_text

        lines.append(children_line)

        # Recursively draw grandchildren for each child
        # We need to interleave the grandchildren properly
        child_trees = []
        for i, child_id in enumerate(children):
            child_indent = indent + (i * 8)
            grandchild_lines = _draw_classic_tree(
                child_id, graph, node_map, visited, child_indent
            )
            # Skip the first line (child node already drawn)
            if len(grandchild_lines) > 1:
                child_trees.append((child_indent, grandchild_lines[1:]))

        # Add all grandchild trees
        if child_trees:
            max_depth = max(len(tree) for _, tree in child_trees)
            for depth in range(max_depth):
                line_parts = []
                for child_indent, tree in child_trees:
                    if depth < len(tree):
                        line_parts.append((child_indent, tree[depth]))

                # Merge line parts into a single line
                if line_parts:
                    merged_line = ""
                    last_pos = 0
                    for pos, text in sorted(line_parts):
                        if pos >= last_pos:
                            merged_line += " " * (pos - last_pos) + text
                            last_pos = pos + len(text)
                    lines.append(merged_line.rstrip())

    return lines


def get_connected_nodes_dfs(db: Session, node_id: int) -> dict:
    """Get all nodes reachable from the given node using Level 2 approach:
    Fetch all edges, then perform DFS in Python.

    This demonstrates the "Fetch Everything, Then Search in Python" approach
    from the possibilities document. It's easier to understand but less optimal
    than the recursive CTE approach.

    Args:
        db: SQLAlchemy database session
        node_id: ID of the starting node

    Returns:
        Dictionary with source node ID, list of reachable node IDs,
        and total count (timing will be added at the route handler level)

    Technical Details:
        - Single query to fetch ALL edges from database
        - Builds adjacency list in memory
        - Performs Depth-First Search (DFS) recursively in Python
        - Automatically handles cycles with visited set

    Example:
        Given graph: 1 -> 2 -> 3, 1 -> 4
        get_connected_nodes_dfs(db, 1) returns [2, 3, 4]
    """
    from src.models.edge import Edge

    # Step 1: Get ALL edges from the database (just one query!)
    all_edges = db.query(Edge).all()

    # Step 2: Build an "adjacency list" - a dictionary showing connections
    # Example: {1: [2, 3], 2: [4], 3: [5]}
    # Meaning: 1 connects to 2 and 3, node 2 connects to 4, etc.
    graph = {}
    for edge in all_edges:
        if edge.source_node_id not in graph:
            graph[edge.source_node_id] = []
        graph[edge.source_node_id].append(edge.target_node_id)

    # Step 3: Explore the graph using Depth-First Search (DFS)
    visited = set()

    def explore(current_node):
        """Recursively explore all nodes reachable from current_node"""
        # If we've been here before, stop (prevents infinite loops)
        if current_node in visited:
            return

        # Mark this node as visited
        visited.add(current_node)

        # Explore all neighbors (children)
        if current_node in graph:
            for neighbor in graph[current_node]:
                explore(neighbor)  # Recursive call

    # Start exploring from the children of our starting node
    # (We don't include the starting node itself)
    if node_id in graph:
        for child in graph[node_id]:
            explore(child)

    # Return sorted list of visited nodes
    connected_ids = sorted(list(visited))

    return {
        "source_node_id": node_id,
        "connected_node_ids": connected_ids,
        "total_count": len(connected_ids),
    }
