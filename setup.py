#!/usr/bin/env python3
"""
Setup script for Paralegal RAG Agent
"""
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def main():
    """Main setup function"""
    print("Setting up LegalAssistant Agent...")
    
    # Install requirements
    if not install_requirements():
        print("Setup failed!")
        sys.exit(1)
    
    print("Setup complete! Starting the application...")
    
    # Start the application using the main.py entry point
    try:
        import subprocess
        subprocess.run([sys.executable, "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting application: {e}")
        print("Please check the application logs for more details.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
