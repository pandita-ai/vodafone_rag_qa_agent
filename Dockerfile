FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY static/ ./static/

# Create directory for ChromaDB
RUN mkdir -p ./chroma_db

# Set environment variables
ENV PYTHONPATH=/app
ENV CHROMA_DB_IMPL=duckdb+parquet

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "backend/main.py"]
