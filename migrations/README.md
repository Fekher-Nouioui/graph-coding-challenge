# Database Migrations

This directory contains Alembic migration scripts for managing database schema changes.

## Overview

Migrations allow you to version control your database schema and apply changes incrementally across different environments.

## Prerequisites

- Python virtual environment activated
- Database connection configured (via `DATABASE_URL` environment variable)
- MySQL database running

## Common Commands

### View Current Migration Status
```bash
alembic current
```

### View Migration History
```bash
alembic history
```

### Apply All Pending Migrations
```bash
alembic upgrade head
```

### Rollback One Migration
```bash
alembic downgrade -1
```

### Create a New Migration (Auto-generate)
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Create a New Migration (Manual)
```bash
alembic revision -m "Description of changes"
```

## Migration Files

- `env.py` - Alembic environment configuration
- `script.py.mako` - Template for generating new migration files
- `versions/` - Directory containing all migration scripts

## How It Works

1. Alembic tracks the current database version
2. Each migration has an `upgrade()` function to apply changes
3. Each migration has a `downgrade()` function to rollback changes
4. Migrations are applied in chronological order

## Setup

### Docker Compose Setup

When using Docker Compose, migrations can be run inside the container:

```bash
# Apply all migrations
docker-compose exec app alembic upgrade head

# Check current migration version
docker-compose exec app alembic current

# View migration history
docker-compose exec app alembic history
```

### Local Development Setup

For local development without Docker:

```bash
# Activate virtual environment
source .venv/bin/activate

# Set database connection
export DATABASE_URL=mysql+pymysql://appuser:apppassword@localhost:3306/coding_challenge

# Apply migrations
alembic upgrade head
```