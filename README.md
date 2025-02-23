# chatautomation

conda create --name chatautomation python=3.12
conda activate chatautomation
conda deactivate

pip freeze > requirements.txt
pip install langgraph langchain_community
pip install langchain-ollama langchain-qdrant
pip install python-dotenv
pip install fastapi uvicorn
pip install qdrant_client langchain-core
# URL Loder
pip install --upgrade --quiet unstructured
pip install IPython


# Start Qdrant
docker run -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage:z" qdrant/qdrant



# Next release:
Selenium URL Loader:
Using Selenium allows us to load pages that require JavaScript to render.

