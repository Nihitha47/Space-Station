from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.routes import auth, missions, experiments
from api.database import test_connection

# Initialize FastAPI application
app = FastAPI(
    title="Space Station Management System API",
    description="Backend API for managing space station crew, missions, and experiments",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific Angular frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """
    Root endpoint - API health check.
    
    Returns:
        dict: Welcome message and API status
    """
    return {
        "message": "Space Station Management System API",
        "status": "operational",
        "version": "1.0.0",
        "docs": "/docs"
    }


# Health check endpoint
@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint to verify API and database connectivity.
    
    Returns:
        dict: Health status of API and database
    """
    db_status = "connected" if test_connection() else "disconnected"
    
    return {
        "api": "healthy",
        "database": db_status
    }


# Register route modules
app.include_router(auth.router)
app.include_router(missions.router)
app.include_router(experiments.router)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    
    Args:
        request: The request that caused the exception
        exc: The exception that was raised
        
    Returns:
        JSONResponse: Error response with 500 status code
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred",
            "error": str(exc)
        }
    )


# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
