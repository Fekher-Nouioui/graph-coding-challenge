# Graph Navigator Service

A production-ready FastAPI service for managing and traversing directed graphs.

## Table of Contents
- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Separation of Concerns](#separation-of-concerns)
- [Database Schema](#database-schema)
- 
---

## Overview

This service implements a directed graph storage and traversal system. The key challenge solved is **efficient graph traversal using a single recursive SQL query** (MySQL Common Table Expression - CTE).

### Core Capability
Given a starting node, the service can find **all reachable nodes** by following directed edges, handling arbitrary depth and cycles automatically.

**Example:**
```
Graph: A → B → D
       A → C → E

Query: /nodes/A/connected
Result: [B, C, D, E]
```

## Tech Stack

| Component | Technology | Purpose                                  | Java Equivalent             |
|-----------|-----------|------------------------------------------|-----------------------------|
| **Framework** | FastAPI | Web Framework                            | Spring Boot                 |
| **Database** | MySQL 8.0+ | Relational DB with recursive CTE support |                             |
| **ORM** | SQLAlchemy | Database abstraction layer               | Hibernate / JPA             |
| **Validation** | Pydantic | Schema validation (DTOs)                 | Bean Validation API/Records |
| **Migrations** | Alembic | Database version control                 | Flyway                      |
| **Container** | Docker | Application containerization             |                             |
| **Orchestration** | Docker Compose | Multi-container management               |                             |

---

## Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Port 8000 (API) and 3306 (MySQL) available

### 1. Clone and Navigate
```bash
cd coding-challenge
```

### 2. Local Setup
See [local-testing/README.md](local-testing/README.md) for detailed setup instructions.

### 3. Run Database Migrations
See [migrations/README.md](migrations/README.md) for detailed setup instructions.

### 4. Seed the Database
See [scripts/README.md](scripts/README.md) for detailed usage instructions.

---

## Separation of Concerns

- **Routes**: HTTP request/response handling only
- **Services**: Business logic
- **Models**: Database schema definition
- **Schemas**: API contract validation (Pydantic DTOs)

---

## Database Schema

### Nodes Table
```sql
CREATE TABLE nodes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);
```

**Purpose**: Stores graph vertices.

### Edges Table
```sql
CREATE TABLE edges (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    source_node_id BIGINT NOT NULL,
    target_node_id BIGINT NOT NULL,
    FOREIGN KEY (source_node_id) REFERENCES nodes(id) ON DELETE CASCADE,
    FOREIGN KEY (target_node_id) REFERENCES nodes(id) ON DELETE CASCADE,
    INDEX idx_source (source_node_id),  -- CRITICAL for performance
    INDEX idx_target (target_node_id)   -- For reverse queries
);
```

**Purpose**: Stores directed edges (connections).
