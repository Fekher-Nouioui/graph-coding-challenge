# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user to be used later (for security)
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy application source code, migrations, and alembic config
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser migrations/ ./migrations/
COPY --chown=appuser:appuser scripts/ ./scripts/
COPY --chown=appuser:appuser alembic.ini .

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 8000

# Set uvicorn as the entrypoint
ENTRYPOINT ["uvicorn"]

# Default command (production: 4 workers, no reload)
CMD ["src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
