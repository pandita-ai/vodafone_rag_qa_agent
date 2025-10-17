#!/usr/bin/env python3
"""
Replit entry point for the Paralegal RAG Agent
"""
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import and run the main application
from backend.main import app
import uvicorn

if __name__ == "__main__":
    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)
