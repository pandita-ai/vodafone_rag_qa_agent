# LegalAssistant RAG Agent

## Overview

This is a Retrieval-Augmented Generation (RAG) application designed to provide legal assistance by querying a knowledge base of legal documents. The system uses OpenAI's language models combined with ChromaDB for vector storage and retrieval to answer legal questions with relevant context from pre-loaded legal documents.

The application is built as a web service with a FastAPI backend and a single-page application frontend, designed for easy deployment on Replit.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Structure

The application follows a three-tier architecture:

1. **Frontend Layer**: Single-page HTML application with embedded CSS and JavaScript
2. **API Layer**: FastAPI-based REST API that handles query requests
3. **RAG Service Layer**: Core business logic for document retrieval and AI-powered responses

**Rationale**: This separation allows for independent scaling and maintenance of the UI and backend logic. The stateless API design enables easy horizontal scaling if needed.

### Backend Architecture

**Framework**: FastAPI
- **Chosen for**: High performance, automatic API documentation, async support, and modern Python type hints
- **Alternative considered**: Flask (rejected due to lack of native async support and type validation)

**Entry Point Strategy**: Multiple entry points for different deployment scenarios
- `main.py`: Primary Replit entry point that imports from backend
- `backend/main.py`: Core FastAPI application
- `setup.py` and `start_replit.py`: Deployment helpers with dependency installation

**Pros**: Flexible deployment options, easier debugging
**Cons**: Slight complexity in import path management

### RAG (Retrieval-Augmented Generation) Service

**Vector Database**: ChromaDB
- **Implementation**: Dual-mode configuration (persistent/in-memory)
- **Persistent mode**: Uses `PersistentClient` with local file storage (`./chroma_db`)
- **Fallback mode**: In-memory `Client()` if persistent storage fails
- **Rationale**: Provides resilience in different hosting environments while preferring persistent storage for data retention

**Embedding Strategy**: OpenAI Embeddings API
- **Model**: `text-embedding-3-small` (1536 dimensions)
- **Choice**: Uses OpenAI's embedding API for consistent vector representations
- **Collection configuration**: Uses cosine similarity (`hnsw:space: cosine`) for semantic matching
- **Rationale**: Lightweight, cloud-based embeddings reduce deployment image size by avoiding large ML model downloads (sentence-transformers, torch, etc.)
- **Pros**: No local ML models, consistent with LLM provider, smaller deployment footprint
- **Cons**: Requires API calls for embedding generation

**LLM Integration**: OpenAI API
- **Client**: Official OpenAI Python SDK (v1.0+)
- **Chat Model**: `gpt-3.5-turbo` for legal question answering
- **Authentication**: API key via environment variable (`OPENAI_API_KEY`)
- **Rationale**: Industry-standard LLM with strong legal reasoning capabilities

**Document Initialization**: 
- Database is auto-populated on first run if empty
- Documents are generated with OpenAI embeddings during initialization
- Pre-loaded legal knowledge covers: contract law, tort law, property law, criminal law, constitutional law, employment law, family law, intellectual property, corporate law, administrative law, environmental law, tax law, bankruptcy law, immigration law, and health law
- **Metadata structure**: Each document tagged with `type` and `topic` for filtered retrieval

### API Design

**Endpoints**:
- `GET /`: Health check/info endpoint
- `POST /query`: Main query endpoint accepting JSON requests

**Request Model** (`QueryRequest`):
- `query`: String (the legal question)
- `max_results`: Integer (default: 5, number of relevant documents to retrieve)

**Response Model** (`QueryResponse`):
- `answer`: AI-generated response
- `sources`: List of source documents used
- `confidence`: Confidence score of the answer

**Rationale**: Structured request/response models using Pydantic ensure type safety and automatic validation

### CORS Configuration

**Setting**: Permissive (`allow_origins=["*"]`)
- **Rationale**: Designed for demo/development deployment where frontend domain is unknown
- **Production consideration**: Should be restricted to specific domains in production

### Error Handling

**Strategy**: Graceful degradation with fallbacks
- ChromaDB falls back from persistent to in-memory if needed
- HTTP exceptions with 500 status for query failures
- Multiple test scripts (`test_setup.py`, `test_chromadb.py`) for debugging

### Async Support

**Implementation**: Service methods use `async/await` pattern
- `async def query()`: Asynchronous query handling
- **Rationale**: Prevents blocking on I/O operations (API calls, database queries)
- **Framework support**: FastAPI natively supports async handlers

## External Dependencies

### Required Services

1. **OpenAI API**
   - **Purpose**: Language model for generating legal responses
   - **Authentication**: API key stored in environment variable `OPENAI_API_KEY`
   - **Required**: Yes (application will fail without valid key)

### Python Packages

**Core Framework**:
- `fastapi>=0.100.0`: Web framework
- `uvicorn[standard]>=0.20.0`: ASGI server with production extras
- `pydantic>=2.0.0`: Data validation

**AI/ML Stack**:
- `openai>=1.0.0`: OpenAI API client (chat completions and embeddings)
- `chromadb>=0.4.15`: Vector database for document storage and retrieval

**HTTP/Networking**:
- `httpx>=0.24.0`: Async HTTP client
- `requests>=2.28.0`: Synchronous HTTP client

**Utilities**:
- `python-multipart>=0.0.5`: Form data parsing
- `python-dotenv>=1.0.0`: Environment variable management
- `beautifulsoup4>=4.11.0`: HTML parsing
- `lxml>=4.9.0`: XML/HTML parsing backend

### Deployment Optimization

**October 2025 Updates**:
To meet Replit's 8 GiB deployment image size limit for Reserved VM Deployments:

1. **Removed Heavy ML Dependencies**:
   - Eliminated `sentence-transformers` and `huggingface-hub` (saved ~4GB from model downloads)
   - Removed `numpy` dependency (included with chromadb as needed)
   - Switched from local transformer models to cloud-based OpenAI embeddings

2. **Cache Management**:
   - Added `.cache/`, `.pythonlibs/`, and `*.pyc` to `.gitignore`
   - Prevents pip and ML model caches from being included in deployments

3. **Nix Configuration**:
   - Removed unnecessary modules (`web`) to reduce system dependencies
   - Streamlined to essential Python packages only

**Result**: Deployment image size reduced from >8 GiB to well under the limit while maintaining full functionality.

### Storage

**Local File System**:
- `./chroma_db`: ChromaDB persistent storage directory
- Static files served from `static/` directory

**Database**: ChromaDB (embedded, no external database server required)

### Deployment Platform

**Target Platform**: Replit
- Configuration files: `.replit`, `replit.nix`
- Port: 8000 (hard-coded in entry points)
- Host: `0.0.0.0` (accepts external connections)