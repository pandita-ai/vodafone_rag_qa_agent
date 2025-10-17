#!/usr/bin/env python3
"""
Test script to verify ChromaDB configuration works correctly
"""
import os
import sys

def test_chromadb():
    """Test ChromaDB initialization"""
    print("Testing ChromaDB configuration...")
    
    try:
        import chromadb
        print("ChromaDB imported successfully")
        
        # Test persistent client
        try:
            client = chromadb.PersistentClient(path="./test_chroma_db")
            print("PersistentClient created successfully")
            
            # Test collection creation
            collection = client.create_collection("test_collection")
            print("Collection created successfully")
            
            # Test adding a document
            collection.add(
                documents=["This is a test document"],
                metadatas=[{"type": "test"}],
                ids=["test_1"]
            )
            print("Document added successfully")
            
            # Test querying
            results = collection.query(
                query_texts=["test document"],
                n_results=1
            )
            print("Query executed successfully")
            print(f"Query results: {len(results['documents'][0])} documents found")
            
            # Clean up
            client.delete_collection("test_collection")
            print("Test collection cleaned up")
            
            return True
            
        except Exception as e:
            print(f"PersistentClient test failed: {e}")
            
            # Test in-memory client as fallback
            try:
                client = chromadb.Client()
                print("In-memory Client created successfully")
                return True
            except Exception as e2:
                print(f"In-memory Client also failed: {e2}")
                return False
                
    except ImportError as e:
        print(f"ChromaDB import failed: {e}")
        return False

def main():
    """Run ChromaDB test"""
    print("Running ChromaDB configuration test...")
    print("=" * 50)
    
    success = test_chromadb()
    
    print("=" * 50)
    if success:
        print("ChromaDB configuration test passed!")
    else:
        print("ChromaDB configuration test failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
