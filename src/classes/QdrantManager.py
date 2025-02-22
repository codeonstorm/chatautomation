import os
import logging
from dotenv import load_dotenv
from uuid import uuid4
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_core.documents import Document

# Configure logging to store in a file
logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(levelname)s - %(message)s',
  handlers=[
    logging.FileHandler("./logs/qdrant_manager.log"),
    logging.StreamHandler()
  ]
)

class QdrantManager:
  def __init__(self, collection_name="demo_collection", vector_size=3072, distance_metric=Distance.COSINE, model_name="llama3.2"):
    """Initialize the QdrantManager with collection configuration."""
    try:
      load_dotenv()
      self.qdrant_url = os.getenv("QDRANT_CLIENT_URL")
      self.qdrant_api_key = os.getenv("QDRANT_CLIENT_API_KEY")
      self.debug = os.getenv("DEBUG", False)
      
      if not self.qdrant_url or not self.qdrant_api_key:
        raise ValueError("Missing Qdrant configuration in environment variables.")
      
      self.collection_name = collection_name
      self.embeddings = OllamaEmbeddings(model=model_name)
        
      self.client = QdrantClient(url=self.qdrant_url)
      self._initialize_collection(vector_size, distance_metric)
      
      self.vector_store = None  # Lazy initialization
    except Exception as e:
      logging.error(f"Error initializing QdrantManager: {e}")
      raise

  def _initialize_collection(self, vector_size, distance_metric):
    """Create a collection in Qdrant if it doesn't exist."""
    try:
      self.client.create_collection(
        collection_name=self.collection_name,
        vectors_config=VectorParams(size=vector_size, distance=distance_metric),
        )
    except Exception as e:
      logging.warning(f"Error initializing collection: {e}")

  def _initialize_vector_store(self):
    """Lazy initialization of vector store."""
    if self.vector_store is None:
      self.vector_store = QdrantVectorStore(
        client=self.client, collection_name=self.collection_name, embedding=self.embeddings
      )

  def add_documents(self, documents):
    """Add documents to the Qdrant vector store."""
    try:
      self._initialize_vector_store()
      uuids = [str(uuid4()) for _ in range(len(documents))]
      self.vector_store.add_documents(documents=documents, ids=uuids)
      if self.debug: logging.info("Documents added successfully.")
      return uuids
    except Exception as e:
      logging.error(f"Error adding documents: {e}")
      return []

  def delete_documents(self, doc_ids):
    """Delete documents from the Qdrant vector store."""
    try:
      self._initialize_vector_store()
      self.vector_store.delete(ids=doc_ids)
      if self.debug: logging.info("Documents deleted successfully.")
    except Exception as e:
      logging.error(f"Error deleting documents: {e}")

  def search(self, query, top_k=2):
    """Perform a similarity search in the vector store."""
    try:
      self._initialize_vector_store()
      results = self.vector_store.similarity_search(query, k=top_k)
      if self.debug: logging.info("Search executed successfully.")
      return results
    except Exception as e:
      logging.error(f"Error performing search: {e}")
      return []

# Usage Example
if __name__ == "__main__":
  try:
      qdrant_manager = QdrantManager()
      
      # Create documents
      documents = [
          Document(
              page_content="I had chocolate chip pancakes and scrambled eggs for breakfast this morning.",
              metadata={"source": "tweet"},
          ),
          Document(
              page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees.",
              metadata={"source": "news"},
          ),
      ]
      
      # Add documents to the store
      added_ids = qdrant_manager.add_documents(documents)
      # if self.debulogging.info(f"Added document IDs: {added_ids}")
      
      # Perform a similarity search
      search_results = qdrant_manager.search("LangChain provides abstractions to make working with LLMs easy", top_k=2)
      for res in search_results:
          logging.info(f"* {res.page_content} [{res.metadata}]")
  except Exception as e:
      logging.critical(f"Error in main execution: {e}")
