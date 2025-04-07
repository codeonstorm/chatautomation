#!/bin/bash
# Install dependencies
cd ./frontend
npm run dev


# pip install -r requirements.txt

# Run the FastAPI application
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
conda activate chatautomation
cd ../backend
uvicorn main:app --reload

