#!/usr/bin/env python3
"""
Robust startup script for Replit deployment
"""
import sys
import os
import subprocess
import traceback

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False

def check_dependencies():
    """Check if all required dependencies are available"""
    required_modules = ['fastapi', 'uvicorn', 'openai', 'chromadb']
    missing = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        return False
    
    print("All dependencies available")
    return True

def setup_python_path():
    """Setup Python path for imports"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(current_dir, 'backend')
    
    # Add paths to sys.path
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    
    print(f"Python path configured: {current_dir}, {backend_dir}")

def start_application():
    """Start the FastAPI application"""
    try:
        # Try importing from backend package
        from backend.main import app
        import uvicorn
        
        print("Starting FastAPI server...")
        print("Server will be available at: http://0.0.0.0:5000")
        print("API docs will be available at: http://0.0.0.0:5000/docs")
        print("Demo interface will be available at: http://0.0.0.0:5000/demo")
        
        uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Full traceback:")
        traceback.print_exc()
        
        # Try alternative import method
        print("\nTrying alternative import method...")
        try:
            # Add backend to path and import directly
            backend_path = os.path.join(os.path.dirname(__file__), 'backend')
            sys.path.insert(0, backend_path)
            
            import main as backend_main
            import uvicorn
            
            print("Starting FastAPI server (alternative method)...")
            uvicorn.run(backend_main.app, host="0.0.0.0", port=5000, log_level="info")
            
        except Exception as e2:
            print(f"Alternative import also failed: {e2}")
            print("Full traceback:")
            traceback.print_exc()
            sys.exit(1)

def main():
    """Main startup function"""
    print("Starting LegalAssistant Agent...")
    print("=" * 50)
    
    # Setup Python path
    setup_python_path()
    
    # Check dependencies
    if not check_dependencies():
        print("Installing missing dependencies...")
        if not install_dependencies():
            print("Failed to install dependencies. Exiting.")
            sys.exit(1)
    
    # Check environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set. The app will start but queries may fail.")
        print("Please set your OpenAI API key in Replit Secrets.")
    else:
        print("OpenAI API key found")
    
    print("=" * 50)
    
    # Start the application
    start_application()

if __name__ == "__main__":
    main()
