# Paralegal AI Assistant - RAG Agent Demo

A sleek, intelligent legal research assistant powered by Retrieval-Augmented Generation (RAG) technology. This demo showcases how AI can assist paralegals with legal research and document analysis.

## 🚀 Features

- **Intelligent Legal Research**: Ask questions about contract law, tort law, property law, criminal law, and more
- **Source Attribution**: Every answer includes relevant sources with confidence scores
- **Modern UI**: Sleek, responsive design inspired by Physical Intelligence's aesthetic
- **Easy Deployment**: Docker-based deployment for seamless integration
- **API Ready**: RESTful API for marketplace integration

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │───▶│   FastAPI       │───▶│   RAG Service   │
│   (HTML/CSS/JS) │    │   Backend       │    │   (ChromaDB +    │
│                 │    │                 │    │    OpenAI)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose
- OpenAI API Key

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd vodafone_agent_marketplace
```

### 2. Environment Configuration

```bash
cp env.example .env
# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run with Docker

```bash
# Build and start the application
docker-compose up --build

# The application will be available at http://localhost:8000
```

### 4. Access the Demo

- **Web Interface**: http://localhost:8000/demo
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🛠️ Development Setup

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
cd backend
python main.py
```

### API Endpoints

- `GET /` - API information
- `POST /query` - Submit legal questions
- `GET /health` - Health check
- `GET /demo` - Serve the web interface

### Example API Usage

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What are the elements of negligence?",
       "max_results": 5
     }'
```

## 📊 Legal Knowledge Base

The demo includes sample legal documents covering:

- **Contract Law**: Formation, consideration, breach
- **Tort Law**: Negligence, standard of care
- **Property Law**: Adverse possession, real estate
- **Criminal Law**: Assault, battery, elements
- **Constitutional Law**: First Amendment, civil rights
- **Employment Law**: At-will employment, workplace rights
- **Family Law**: Divorce, custody, support
- **Intellectual Property**: Copyright, trademarks

## 🎨 UI Design

The interface features:

- **Modern Gradient Background**: Purple-blue gradient for visual appeal
- **Glass Morphism**: Frosted glass effect with backdrop blur
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Elements**: Hover effects, smooth transitions
- **Example Queries**: Pre-built questions to get started
- **Confidence Scoring**: Visual indicators of answer reliability

## 🔧 Customization

### Adding New Legal Documents

Edit `backend/rag_service.py` and add documents to the `legal_documents` list:

```python
{
    "id": "unique_id",
    "content": "Legal document content...",
    "metadata": {"type": "law_category", "topic": "specific_topic"}
}
```

### Modifying the UI

- **Colors**: Update CSS variables in `static/index.html`
- **Layout**: Modify the HTML structure and CSS classes
- **Functionality**: Extend the JavaScript functions

### API Integration

The API is designed for easy marketplace integration:

```python
# Example integration code
import requests

def query_legal_agent(question):
    response = requests.post(
        "http://your-agent-url/query",
        json={"query": question, "max_results": 5}
    )
    return response.json()
```

## 🚀 Deployment Options

### Docker Deployment
```bash
docker-compose up -d
```

### Cloud Deployment
- **Heroku**: Add Procfile and deploy
- **AWS**: Use ECS or Lambda
- **Google Cloud**: Cloud Run or App Engine
- **Azure**: Container Instances

### Production Considerations

1. **Environment Variables**: Secure API key management
2. **Database Persistence**: Mount ChromaDB volume
3. **Scaling**: Use load balancers for multiple instances
4. **Monitoring**: Add logging and health checks
5. **Security**: Implement authentication and rate limiting

## 📈 Performance Optimization

- **Embedding Caching**: Cache embeddings for faster retrieval
- **Database Indexing**: Optimize ChromaDB queries
- **Response Streaming**: Stream responses for better UX
- **CDN**: Use CDN for static assets

## 🔒 Security Considerations

- **API Key Protection**: Never expose OpenAI keys in frontend
- **Input Validation**: Sanitize user queries
- **Rate Limiting**: Prevent API abuse
- **CORS Configuration**: Restrict origins in production

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For questions or support, please contact the development team or create an issue in the repository.

---

**Built with ❤️ for the legal community**
