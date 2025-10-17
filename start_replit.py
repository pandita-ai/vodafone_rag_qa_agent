#!/usr/bin/env python3
"""
Simple startup script for Replit deployment
"""
import sys
import os
import subprocess

def main():
    print("🚀 Starting Paralegal RAG Agent...")
    
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(current_dir, 'backend')
    sys.path.insert(0, current_dir)
    sys.path.insert(0, backend_dir)
    
    # Install requirements if needed
    try:
        import fastapi
        import uvicorn
        import openai
        print("✅ Dependencies already installed")
    except ImportError:
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed")
    
    # Import and start the app
    try:
        from backend.main import app
        import uvicorn
        
        print("🎯 Starting FastAPI server...")
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Trying alternative import...")
        
        # Try direct import
        try:
            import main as backend_main
            import uvicorn
            print("🎯 Starting FastAPI server (alternative)...")
            uvicorn.run(backend_main.app, host="0.0.0.0", port=8000)
        except Exception as e2:
            print(f"❌ Alternative import failed: {e2}")
            sys.exit(1)

if __name__ == "__main__":
    main()
