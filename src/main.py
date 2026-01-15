"""Graph Navigator Service - FastAPI Application.

A production-ready service for managing and traversing directed graphs.
Built with FastAPI, SQLAlchemy, and MySQL.
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.routes import nodes

# Create FastAPI application
app = FastAPI(
    title="Graph Navigator Service",
    version="1.0.0",
)

# Include routers
app.include_router(nodes.router)


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint for monitoring and load balancers.

    Returns:
        Health status
    """
    return {"status": "healthy", "service": "graph-navigator"}


# Global exception handler for better error responses
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle unexpected exceptions gracefully."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred. Please try again later.",
        },
    )
