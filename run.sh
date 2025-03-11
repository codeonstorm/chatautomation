#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Run the FastAPI application
uvicorn main:app --reload --host 0.0.0.0 --port 8000

