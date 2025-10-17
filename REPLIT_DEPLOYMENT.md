# Deploy to Replit - Paralegal RAG Agent

## 🚀 Quick Deployment to Replit

### Step 1: Create a New Replit
1. Go to [replit.com](https://replit.com)
2. Click "Create Repl"
3. Choose "Import from GitHub" or "Create Repl"
4. If creating new, select "Python" template

### Step 2: Upload Your Code
1. **Option A: GitHub Import**
   - Upload this entire folder to GitHub
   - Import from GitHub in Replit

2. **Option B: Manual Upload**
   - Copy all files from this project to your Replit
   - Make sure to include all files in the correct structure

### Step 3: Set Environment Variables
1. In Replit, go to the "Secrets" tab (lock icon)
2. Add your OpenAI API key:
   - Key: `OPENAI_API_KEY`
   - Value: `your_actual_openai_api_key_here`

### Step 4: Install Dependencies
1. Replit will automatically install from `requirements.txt`
2. If not, run in the Shell: `pip install -r requirements.txt`

### Step 5: Run the Application
1. Click the "Run" button in Replit
2. The app will start on port 8000
3. Replit will provide a public URL

## 📁 Required Files Structure
```
your-repl/
├── main.py                 # Replit entry point
├── .replit                 # Replit configuration
├── replit.nix             # Nix configuration
├── requirements.txt        # Python dependencies
├── backend/
│   ├── main.py            # FastAPI application
│   └── rag_service.py     # RAG service
├── static/
│   └── index.html         # Frontend UI
└── README.md              # Documentation
```

## 🔧 Configuration Files

### .replit
```toml
run = "python backend/main.py"
entrypoint = "main.py"
modules = ["python-3.11"]

[nix]
channel = "stable-24_05"

[deployment]
run = ["sh", "-c", "python backend/main.py"]
```

### replit.nix
```nix
{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.setuptools
    pkgs.python311Packages.wheel
  ];
}
```

## 🌐 Access Your App
Once deployed, you'll get a public URL like:
- `https://your-repl-name.your-username.repl.co`
- The web interface will be at: `https://your-repl-name.your-username.repl.co/demo`
- API docs at: `https://your-repl-name.your-username.repl.co/docs`

## 🎯 Features Available
- ✅ **Web Interface**: Beautiful legal research interface
- ✅ **API Endpoints**: RESTful API for integration
- ✅ **Legal Knowledge Base**: Pre-loaded with legal documents
- ✅ **RAG Functionality**: Intelligent document retrieval
- ✅ **Source Attribution**: Every answer includes sources
- ✅ **Confidence Scoring**: Reliability indicators

## 🔒 Security Notes
- Your OpenAI API key is stored securely in Replit Secrets
- The app runs in a sandboxed environment
- All data is processed securely

## 🚀 Marketplace Integration
The API is ready for integration with your Pandita AI marketplace:
- Endpoint: `POST /query`
- Request: `{"query": "legal question", "max_results": 5}`
- Response: `{"answer": "...", "sources": [...], "confidence": 0.95}`

## 📞 Support
If you encounter any issues:
1. Check the Replit console for error messages
2. Verify your OpenAI API key is set correctly
3. Ensure all files are uploaded properly
4. Check that dependencies installed successfully

---

**Ready to deploy! 🚀**
