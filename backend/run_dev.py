"""
Local development server for Space Station Management System API.
Run this script to start the FastAPI server locally with hot reload.
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Check if database credentials are configured
    if not os.getenv("DB_HOST"):
        print("⚠️  WARNING: Database environment variables not configured!")
        print("📝 Please create a .env file based on .env.example")
        print()
    
    print("🚀 Starting Space Station Management System API...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("📖 Alternative Docs: http://localhost:8000/redoc")
    print("🏥 Health Check: http://localhost:8000/health")
    print()
    
    # Start the server with hot reload
    uvicorn.run(
        "api.index:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
