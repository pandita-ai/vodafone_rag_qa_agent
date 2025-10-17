#!/usr/bin/env python3
"""
Test script to verify the setup works correctly
"""
import sys
import os

def test_imports():
    """Test all critical imports"""
    print("Testing imports...")
    
    try:
        import fastapi
        print("FastAPI imported successfully")
    except ImportError as e:
        print(f"FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("Uvicorn imported successfully")
    except ImportError as e:
        print(f"Uvicorn import failed: {e}")
        return False
    
    try:
        import openai
        print("OpenAI imported successfully")
    except ImportError as e:
        print(f"OpenAI import failed: {e}")
        return False
    
    try:
        import chromadb
        print("ChromaDB imported successfully")
    except ImportError as e:
        print(f"ChromaDB import failed: {e}")
        return False
    
    try:
        import sentence_transformers
        print("Sentence Transformers imported successfully")
    except ImportError as e:
        print(f"Sentence Transformers import failed: {e}")
        return False
    
    return True

def test_backend_imports():
    """Test backend module imports"""
    print("\nTesting backend imports...")
    
    # Add backend to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(current_dir, 'backend')
    sys.path.insert(0, backend_dir)
    
    try:
        from main import app
        print("Backend main module imported successfully")
    except ImportError as e:
        print(f"Backend main import failed: {e}")
        return False
    
    try:
        from rag_service import RAGService
        print("RAG service imported successfully")
    except ImportError as e:
        print(f"RAG service import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment setup"""
    print("\nTesting environment...")
    
    if os.getenv("OPENAI_API_KEY"):
        print("OpenAI API key found")
    else:
        print("OpenAI API key not set (this is expected in test environment)")
    
    return True

def main():
    """Run all tests"""
    print("Running setup tests...")
    print("=" * 50)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test backend imports
    if not test_backend_imports():
        all_passed = False
    
    # Test environment
    if not test_environment():
        all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("All tests passed! Setup is ready for deployment.")
    else:
        print("Some tests failed. Please check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
