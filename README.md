# LegalAssistant Agent

A sophisticated legal research assistant powered by advanced AI and retrieval-augmented generation (RAG). Built with FastAPI and deployed on Replit, this agent provides comprehensive legal knowledge across multiple practice areas.

## Features

- **Comprehensive Legal Database**: 50+ legal documents covering 12 major practice areas
- **Intelligent Search**: Semantic search with relevance scoring and source attribution
- **Modern Interface**: Dark theme inspired by Physical Intelligence design
- **API Integration**: RESTful API ready for marketplace integration
- **Real-time Processing**: Fast query responses with confidence scoring

## Legal Practice Areas

- Contract Law
- Tort Law
- Property Law
- Criminal Law
- Constitutional Law
- Employment Law
- Family Law
- Intellectual Property
- Corporate Law
- Administrative Law
- Environmental Law
- Tax Law
- Bankruptcy Law
- Immigration Law
- Health Law

## Technology Stack

- **Backend**: FastAPI with Python 3.11
- **Vector Database**: ChromaDB with persistent storage
- **AI Model**: OpenAI GPT-3.5-turbo
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Frontend**: HTML5 with modern CSS and JavaScript
- **Deployment**: Replit with automatic dependency management

## Quick Start

### Deploy to Replit

1. Visit [replit.com](https://replit.com) and create a new Repl
2. Import from GitHub: `https://github.com/pandita-ai/vodafone_rag_qa_agent`
3. Set your OpenAI API key in Replit Secrets:
   - Key: `OPENAI_API_KEY`
   - Value: `your_openai_api_key_here`
4. Click "Run" to start the application

### Local Development

```bash
git clone https://github.com/pandita-ai/vodafone_rag_qa_agent.git
cd vodafone_rag_qa_agent
cp env.example .env
# Add your OPENAI_API_KEY to .env
pip install -r requirements.txt
python start_replit.py
```

## API Endpoints

- `GET /` - API status
- `POST /query` - Submit legal questions
- `GET /demo` - Web interface
- `GET /docs` - Interactive API documentation
- `GET /health` - Health check

### Query Example

```bash
curl -X POST "https://your-app.repl.co/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the elements of negligence?",
    "max_results": 5
  }'
```

## Project Structure

```
vodafone_agent_marketplace/
├── backend/
│   ├── main.py              # FastAPI application
│   └── rag_service.py       # RAG service with ChromaDB
├── static/
│   └── index.html           # Frontend interface
├── start_replit.py          # Main startup script
├── requirements.txt         # Python dependencies
├── .replit                  # Replit configuration
└── README.md               # This file
```

## Configuration

The application uses environment variables for configuration:

- `OPENAI_API_KEY`: Required OpenAI API key for AI responses
- `PYTHONPATH`: Automatically configured for module imports

## Dependencies

- fastapi>=0.100.0
- uvicorn[standard]>=0.20.0
- openai>=1.0.0
- chromadb>=0.4.15
- sentence-transformers>=2.2.0
- python-dotenv>=1.0.0

## Deployment Notes

- Optimized for Replit deployment with automatic dependency installation
- ChromaDB configured with persistent storage and fallback to in-memory
- Robust error handling with multiple import strategies
- No Docker dependencies - streamlined for cloud deployment

## License

MIT License - see LICENSE file for details.

## Support

For deployment issues, check the Replit console for error messages and ensure your OpenAI API key is properly configured.
