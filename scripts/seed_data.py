"""Seed script to populate the database with a multi-level graph structure.

This script creates a directed graph that is 5+ levels deep with multiple
outgoing edges per node to demonstrate the system's traversal capabilities.

Graph Structure:
- Level 0: 1 root node
- Level 1: 3 children of root
- Level 2: 9 children (3 per level 1 node)
- Level 3: 18 children (2 per level 2 node)
- Level 4: 36 children (2 per level 3 node)
- Level 5: 50 children (varying children per level 4 node)

Total: ~117 nodes, ~115 edges
"""
import sys
from pathlib import Path

# Add project root to path to allow imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.database import SessionLocal
from src.models.node import Node
from src.models.edge import Edge


def clear_database(db):
    """Clear all existing data from the database."""
    print("Clearing existing data...")
    db.query(Edge).delete()
    db.query(Node).delete()
    db.commit()
    print("Database cleared.")


def create_graph(db):
    """Create a 5-level deep graph structure."""
    print("Creating graph structure...")

    node_counter = 0

    # Level 0: Root node
    root = Node(name=f"Node {node_counter}")
    node_counter += 1
    db.add(root)
    db.flush()
    print(f"Created Level 0: {root.name} (id={root.id})")

    # Level 1: 3 children
    level_1_nodes = []
    for i in range(3):
        node = Node(name=f"Node {node_counter}")
        node_counter += 1
        db.add(node)
        db.flush()
        db.add(Edge(source_node_id=root.id, target_node_id=node.id))
        level_1_nodes.append(node)
    print(f"Created Level 1: {len(level_1_nodes)} nodes")

    # Level 2: 9 children (3 per L1 node)
    level_2_nodes = []
    for parent in level_1_nodes:
        for i in range(3):
            node = Node(name=f"Node {node_counter}")
            node_counter += 1
            db.add(node)
            db.flush()
            db.add(Edge(source_node_id=parent.id, target_node_id=node.id))
            level_2_nodes.append(node)
    print(f"Created Level 2: {len(level_2_nodes)} nodes")

    # Level 3: 18 children (2 per L2 node)
    level_3_nodes = []
    for parent in level_2_nodes:
        for i in range(2):
            node = Node(name=f"Node {node_counter}")
            node_counter += 1
            db.add(node)
            db.flush()
            db.add(Edge(source_node_id=parent.id, target_node_id=node.id))
            level_3_nodes.append(node)
    print(f"Created Level 3: {len(level_3_nodes)} nodes")

    # Level 4: 36 children (2 per L3 node)
    level_4_nodes = []
    for parent in level_3_nodes:
        for i in range(2):
            node = Node(name=f"Node {node_counter}")
            node_counter += 1
            db.add(node)
            db.flush()
            db.add(Edge(source_node_id=parent.id, target_node_id=node.id))
            level_4_nodes.append(node)
    print(f"Created Level 4: {len(level_4_nodes)} nodes")

    # Level 5: ~50 children (varying 1-2 per L4 node)
    level_5_nodes = []
    for idx, parent in enumerate(level_4_nodes):
        # Vary the number of children (1 or 2) to make it interesting
        num_children = 2 if idx % 3 == 0 else 1
        for i in range(num_children):
            node = Node(name=f"Node {node_counter}")
            node_counter += 1
            db.add(node)
            db.flush()
            db.add(Edge(source_node_id=parent.id, target_node_id=node.id))
            level_5_nodes.append(node)
    print(f"Created Level 5: {len(level_5_nodes)} nodes")

    # Add some cross-level edges for complexity (optional but interesting)
    # Connect some L2 nodes directly to L4 nodes
    if len(level_2_nodes) > 0 and len(level_4_nodes) > 2:
        db.add(Edge(source_node_id=level_2_nodes[0].id, target_node_id=level_4_nodes[0].id))
        db.add(Edge(source_node_id=level_2_nodes[1].id, target_node_id=level_4_nodes[10].id))
        print("Added 2 cross-level edges for complexity")

    db.commit()
    print("\nGraph structure created successfully!")


def print_statistics(db):
    """Print database statistics."""
    node_count = db.query(Node).count()
    edge_count = db.query(Edge).count()

    print("\n" + "=" * 50)
    print("DATABASE STATISTICS")
    print("=" * 50)
    print(f"Total Nodes: {node_count}")
    print(f"Total Edges: {edge_count}")
    print("=" * 50)

    # Show some sample nodes
    root = db.query(Node).filter(Node.name == "Node 0").first()
    if root:
        print(f"\nRoot node: {root.name} (ID: {root.id})")
        print(f"Use this to test: GET /nodes/{root.id}/connected")

    # Show a mid-level node
    mid_node = db.query(Node).filter(Node.id == 5).first()
    if mid_node:
        print(f"\nSample mid-level node: {mid_node.name} (ID: {mid_node.id})")
        print(f"Use this to test: GET /nodes/{mid_node.id}/connected")

    # Show a leaf node
    all_nodes = db.query(Node).all()
    if len(all_nodes) > 10:
        leaf_node = all_nodes[-5]  # Pick a node near the end
        print(f"\nSample leaf node: {leaf_node.name} (ID: {leaf_node.id})")
        print(f"Use this to test: GET /nodes/{leaf_node.id}/connected")
    print()


def main():
    """Main entry point for the seed script."""
    print("\n" + "=" * 50)
    print("GRAPH DATABASE SEEDING SCRIPT")
    print("=" * 50 + "\n")

    db = SessionLocal()
    try:
        clear_database(db)
        create_graph(db)
        print_statistics(db)

        print("\n✅ Seeding completed successfully!")
        print("\nNext steps:")
        print("1. Start the API: docker-compose up")
        print("2. Test connectivity: curl http://localhost:8000/nodes/1/connected")
        print("3. View API docs: http://localhost:8000/docs\n")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
