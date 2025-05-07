# 🤖🧠 Chat Automation Project

## Chatbot Automation: Build Smart AI Chatbots for Your Business – Instantly

Empower your business with **Chatbot Automation**, an advanced AI chatbot builder designed for professionals and brands to create smart, customizable chatbots — no coding required.

Deliver instant, personalized, and engaging experiences to your customers 24/7. Whether it’s answering queries, guiding purchases, or providing support, Chatbot Automation helps you boost conversions, cut response times, and build stronger customer relationships.

### Key Features
- **AI-powered conversations**
- **Personalized responses** using your data (PDFs, Docs, websites)
- **eCommerce integration** (product filtering, ordering, tracking)
- **Email automation** for every chat session

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