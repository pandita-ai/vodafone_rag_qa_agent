#!/bin/bash

echo "Installing Paralegal RAG Agent dependencies..."

# Upgrade pip
python3 -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo "Dependencies installed successfully!"
echo "Starting the application..."

# Start the application
python3 main.py
