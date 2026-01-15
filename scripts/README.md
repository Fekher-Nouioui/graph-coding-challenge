# Database Scripts

This directory contains utility scripts for database operations.

## Prerequisites

- MySQL database running
- Database schema already created (run migrations first)

## Overview

Scripts in this directory help with database initialization, seeding test data, and other maintenance tasks.

## Available Scripts

### `seed_data.py`

Populates the database with a multi-level graph structure for testing and demonstration.

#### What it does:
- Clears existing data from the database
- Creates a 5-level deep directed graph with ~115 nodes and ~116 edges
- Generates nodes named "Node 0", "Node 1", "Node 2", etc.
- Adds cross-level edges for graph complexity

**Graph Structure:**
- Level 0: 1 root node (Node 0)
- Level 1: 3 children
- Level 2: 9 children (3 per Level 1 node)
- Level 3: 18 children (2 per Level 2 node)
- Level 4: 36 children (2 per Level 3 node)
- Level 5: ~48 children (1-2 per Level 4 node)

#### Usage

With Docker compose:
```bash
docker-compose exec app python scripts/seed_data.py
```

Local development:
```bash
source .venv/bin/activate
export DATABASE_URL=mysql+pymysql://appuser:apppassword@localhost:3306/coding_challenge
python scripts/seed_data.py
```