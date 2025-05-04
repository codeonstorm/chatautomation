# Chat Automation Project

## Environment Setup
```bash
# Create and activate conda environment
conda create --name chatautomation python=3.12
conda activate chatautomation
conda deactivate
```

## Package Installation
### Core Dependencies
```bash
pip freeze > requirements.txt
pip install langgraph langchain_community
pip install langchain-ollama langchain-qdrant
pip install python-dotenv
pip install fastapi uvicorn
pip install qdrant_client langchain-core
```

### Document Processing
```bash
pip install --upgrade --quiet unstructured
pip install IPython
```

### Web & Database
```bash
pip install WebSocket
pip install sqlmodel
pip install mysql-connector-python
pip install alembic
pip install python-multipart  # for FastAPI
```

### Web Crawling
```bash
pip install crawl4ai
crawl4ai-setup  # Run the setup command
```

### Message Queue
```bash
pip install -U dramatiq[rabbitmq]
# Access RabbitMQ dashboard: http://localhost:15672/#
# Default credentials:
# Username: guest
# Password: guest
```

### Authentication & Security
```bash
pip install python-jose[cryptography] passlib
pip install bcrypt
# Generate secret key: openssl rand -hex 32
```

## Docker Services
### Qdrant Vector Database
```bash
docker run -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage:z" qdrant/qdrant
```

## Database Migrations
```bash
alembic init migrations  # Initialize alembic
alembic revision --autogenerate -m "initial"
alembic upgrade head
alembic history
alembic stamp head
```

## pip install pypdf python-docx python-pptx

## Development
```bash
uvicorn chatbot1:app --reload  # Run server
black .  # Format code
```

## Security Notes
### JWT Authentication
- Ensures authenticated access to WebSocket communication
- Prevents unauthorized endpoint access
- Uses secure signing algorithms (HS256, RS256)

### Password Security
- Uses bcrypt for secure password hashing
- Includes automatic salt generation
- Protects against rainbow table attacks
