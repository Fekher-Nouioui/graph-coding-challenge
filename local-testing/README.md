# Local Development Environment

This directory contains the Docker Compose setup for local development and testing with hot-reload enabled.

## Prerequisites

- Docker (version 20.10+)
- Docker Compose (version 2.0+)

## Quick Start

1. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Configure credentials:**
   Edit the `.env` file and replace the placeholder values with your actual credentials:
   ```bash
   # Update these values in .env:
   MYSQL_ROOT_PASSWORD=the_root_password_of_your_choice
   MYSQL_PASSWORD=the_password_of_your_choice
   ```

3. **Start the services:**
   ```bash
   docker-compose up
   ```

4. **Access the application:**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - MySQL: http://localhost:3306

## Services

### Application (app)
- **Image:** Built from `../Dockerfile`
- **Port:** 8000
- **Environment:** Development mode with **hot-reload enabled** (`--reload` flag)
- **Workers:** 1 (single worker for hot-reload compatibility)
- **Volume mount:** `../src/` directory mounted to `/app/src/` for instant code changes
- **Import path:** `src.main:app` (FastAPI app instance)
- **Depends on:** MySQL database (waits for health check)

### Database (db)
- **Image:** MySQL 8.0
- **Port:** 3306
- **Database:** coding_challenge
- **User:** appuser
- **Data persistence:** Named volume `mysql_data`

## Configuration

All configuration is managed through the [.env](.env) file. See [.env.example](.env.example) for required variables:

- `MYSQL_ROOT_PASSWORD` - MySQL root password
- `MYSQL_DATABASE` - Database name
- `MYSQL_USER` - Application database user
- `MYSQL_PASSWORD` - Application user password
- `DATABASE_URL` - Full connection string for the application

**Note:** The `.env` file is gitignored and shouldn't be committed to version control.

## Data Persistence

### MySQL Volume
The MySQL database uses a Docker named volume (`mysql_data`) for data persistence. This means:

- ✅ **Data survives container restarts** - `docker-compose down` and `docker-compose up` won't lose data
- ✅ **Data survives container deletion** - Removing the container keeps the data
- ✅ **Data survives image updates** - Upgrading MySQL image preserves your data
- ❌ **Data is removed with `-v` flag** - `docker-compose down -v` deletes all data permanently

## Useful Commands

### Start services in detached mode
```bash
docker-compose up -d
```

### View logs
```bash
docker-compose logs -f app
docker-compose logs -f db
```

### Stop services
```bash
docker-compose down
```

### Stop services and remove volumes (deletes all data)
```bash
docker-compose down -v
```

### Rebuild images
```bash
docker-compose up --build
```

## Database Management

### Connect to MySQL
```bash
# As appuser
docker-compose exec db mysql -u appuser -p
# Password: apppassword (from .env)

# As root
docker-compose exec db mysql -u root -p
# Password: from MYSQL_ROOT_PASSWORD in .env
```

## Network

All services are connected via the `app-network` bridge network, allowing:
- App to connect to DB using hostname `db`
- Service isolation from other Docker containers
- Custom DNS resolution between services
