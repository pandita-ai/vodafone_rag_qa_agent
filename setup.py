#!/usr/bin/env python3
"""
Setup script for Paralegal RAG Agent
"""
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("🚀 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def main():
    """Main setup function"""
    print("🎯 Setting up Paralegal RAG Agent...")
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed!")
        sys.exit(1)
    
    print("🎉 Setup complete! Starting the application...")
    
    # Start the application
    try:
        import uvicorn
        from backend.main import app
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please make sure all dependencies are installed correctly.")
        sys.exit(1)

if __name__ == "__main__":
    main()
