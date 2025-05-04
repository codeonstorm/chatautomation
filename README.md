# Chat Automation Project

## Environment Setup
```bash
# Create and activate conda environment
conda create --name chatautomation python=3.12
conda activate chatautomation
conda deactivate
pip install -r requirements.txt
```

## Running the Application

### Backend
```bash
# Start FastAPI server
cd backend
uvicorn main:app --reload

# Start Dramatiq worker
cd backend
dramatiq tasks.tasks
```

### Frontend
```bash
# Start Next.js development server
cd frontent
npm run dev
```