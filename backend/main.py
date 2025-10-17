from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from rag_service import RAGService
import uvicorn

load_dotenv()

app = FastAPI(title="Paralegal RAG Agent", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG service
rag_service = RAGService()

class QueryRequest(BaseModel):
    query: str
    max_results: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: list
    confidence: float

@app.get("/")
async def root():
    return {"message": "Paralegal RAG Agent API"}

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    try:
        result = await rag_service.query(request.query, request.max_results)
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            confidence=result["confidence"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/demo")
async def serve_demo():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
