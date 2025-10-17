import os
import openai
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import json
from typing import List, Dict, Any
import asyncio
import numpy as np

class RAGService:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db"
        ))
        
        # Get or create collection
        try:
            self.collection = self.chroma_client.get_collection("legal_documents")
        except:
            self.collection = self.chroma_client.create_collection("legal_documents")
        
        # Initialize database if empty
        if self.collection.count() == 0:
            self._initialize_database()
    
    def _initialize_database(self):
        """Initialize the database with sample legal documents"""
        legal_documents = [
            {
                "id": "contract_formation_1",
                "content": "A contract is formed when there is an offer, acceptance, and consideration. The offer must be clear and definite, and the acceptance must be unqualified and communicated to the offeror.",
                "metadata": {"type": "contract_law", "topic": "contract_formation"}
            },
            {
                "id": "contract_formation_2", 
                "content": "Consideration is something of value given in exchange for a promise. It can be money, goods, services, or a promise to do or not do something.",
                "metadata": {"type": "contract_law", "topic": "consideration"}
            },
            {
                "id": "tort_negligence_1",
                "content": "Negligence requires four elements: duty of care, breach of duty, causation, and damages. The defendant must owe a duty of care to the plaintiff, breach that duty, and the breach must cause the plaintiff's damages.",
                "metadata": {"type": "tort_law", "topic": "negligence"}
            },
            {
                "id": "tort_negligence_2",
                "content": "The standard of care is what a reasonable person would do under the same circumstances. Professionals are held to a higher standard of care based on their expertise.",
                "metadata": {"type": "tort_law", "topic": "standard_of_care"}
            },
            {
                "id": "property_adverse_possession_1",
                "content": "Adverse possession allows someone to gain title to real property by occupying it openly, notoriously, exclusively, and continuously for the statutory period, usually 10-20 years depending on jurisdiction.",
                "metadata": {"type": "property_law", "topic": "adverse_possession"}
            },
            {
                "id": "criminal_assault_1",
                "content": "Assault is the intentional creation of a reasonable apprehension of imminent harmful or offensive contact. Battery is the actual harmful or offensive contact. Assault can occur without battery.",
                "metadata": {"type": "criminal_law", "topic": "assault_battery"}
            },
            {
                "id": "constitutional_first_amendment_1",
                "content": "The First Amendment protects freedom of speech, religion, press, assembly, and petition. However, these rights are not absolute and can be limited by compelling government interests.",
                "metadata": {"type": "constitutional_law", "topic": "first_amendment"}
            },
            {
                "id": "employment_at_will_1",
                "content": "Employment at will means either the employer or employee can terminate the employment relationship at any time, for any reason, or for no reason at all, unless there is a contract stating otherwise.",
                "metadata": {"type": "employment_law", "topic": "at_will_employment"}
            },
            {
                "id": "family_divorce_1",
                "content": "No-fault divorce allows couples to dissolve their marriage without proving fault or wrongdoing by either party. Most states require a waiting period before the divorce can be finalized.",
                "metadata": {"type": "family_law", "topic": "divorce"}
            },
            {
                "id": "intellectual_property_copyright_1",
                "content": "Copyright protects original works of authorship fixed in a tangible medium of expression. It gives the owner exclusive rights to reproduce, distribute, perform, and display the work.",
                "metadata": {"type": "intellectual_property", "topic": "copyright"}
            }
        ]
        
        # Add documents to collection
        for doc in legal_documents:
            self.collection.add(
                documents=[doc["content"]],
                metadatas=[doc["metadata"]],
                ids=[doc["id"]]
            )
    
    async def query(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """Query the RAG system with a user question"""
        
        # Generate embedding for the query
        query_embedding = self.embedding_model.encode([query]).tolist()[0]
        
        # Search for similar documents
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=max_results
        )
        
        # Extract relevant documents
        documents = results['documents'][0] if results['documents'] else []
        metadatas = results['metadatas'][0] if results['metadatas'] else []
        distances = results['distances'][0] if results['distances'] else []
        
        # Prepare context for LLM
        context = "\n\n".join(documents)
        
        # Generate answer using OpenAI
        prompt = f"""
        You are a legal assistant helping paralegals with legal research. 
        Based on the following legal documents, answer the user's question accurately and professionally.
        
        Legal Documents:
        {context}
        
        User Question: {query}
        
        Please provide a clear, accurate answer based on the legal documents provided. 
        If the documents don't contain enough information to answer the question, say so.
        Include relevant citations to the legal concepts mentioned.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable legal assistant specializing in helping paralegals with legal research and document analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            answer = response.choices[0].message.content
            
            # Calculate confidence based on similarity scores
            confidence = 1.0 - np.mean(distances) if distances else 0.5
            
            # Prepare sources
            sources = []
            for i, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances)):
                sources.append({
                    "content": doc[:200] + "..." if len(doc) > 200 else doc,
                    "metadata": metadata,
                    "relevance_score": 1.0 - distance
                })
            
            return {
                "answer": answer,
                "sources": sources,
                "confidence": min(confidence, 1.0)
            }
            
        except Exception as e:
            return {
                "answer": f"I apologize, but I encountered an error while processing your request: {str(e)}",
                "sources": [],
                "confidence": 0.0
            }
