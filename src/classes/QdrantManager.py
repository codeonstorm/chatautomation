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
    # logging.FileHandler("../../logs/qdrant_manager.log"),
    logging.StreamHandler()
  ]
)

class QdrantManager:
  client = None  #static variable
  
  def __init__(self, model_name="llama3.2"):
    """Initialize the QdrantManager with collection configuration."""
    try:
      load_dotenv()
      self.qdrant_url = os.getenv("QDRANT_CLIENT_URL")
      self.qdrant_api_key = os.getenv("QDRANT_CLIENT_API_KEY")
      self.debug = os.getenv("DEBUG", False)
      self.vector_store = {}  # Lazy initialization
      
      if not self.qdrant_url or not self.qdrant_api_key:
        raise ValueError("Missing Qdrant configuration in environment variables.")
      
      self.embeddings = OllamaEmbeddings(model=model_name)
      if QdrantManager.client is None:
        QdrantManager.client = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key)

    except Exception as e:
      logging.error(f"Error initializing QdrantManager: {e}")
      raise

  def get_vector_store(self, collection_name="chatbot") -> QdrantVectorStore:
    """Get the Qdrant vector store."""
    try:
      self._initialize_vector_store(collection_name)
      return self.vector_store[collection_name]
    except Exception as e:
      logging.error(f"Error getting vector store: {e}")
      return
    
  def _initialize_vector_store(self, collection_name):
    """Lazy initialization of vector store."""
    if collection_name not in self.vector_store:
      self.vector_store[collection_name] = QdrantVectorStore.from_existing_collection(
        # QdrantManager.client,
        embedding=self.embeddings,
        collection_name=collection_name,
        prefer_grpc=True,
        url=self.qdrant_url,
        api_key=self.qdrant_api_key,
      )

  def create_new_collection(self, collection_name, vector_size=3072, distance_metric=Distance.COSINE) -> bool:
    """Create a new collection in Qdrant."""
    try:
      existing_collections = QdrantManager.client.get_collections()
      if collection_name in [col.name for col in existing_collections.collections]:
        if self.debug:
          logging.info(f"Collection {collection_name} already exists.")
        return

      QdrantManager.client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=distance_metric),
      )
      return True
    except Exception as e:
      logging.error(f"Error creating collection: {e}")
      return False


# Usage Example
if __name__ == "__main__":
  qdrantManager = QdrantManager()
  vector_store = qdrantManager.get_vector_store("chatbot")
   
  # Prepare your documents, metadata, and IDs
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
  # added_ids = qdrant.add_documents(documents)
  # if self.debulogging.info(f"Added document IDs: {added_ids}")

  retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 2})
  data = retriever.invoke("Stealing from the bank is a crime")
  print(data)


  # try:
  #   qdrant_manager = QdrantManager()
      
  #   # Create documents
  #   documents = [
  #     Document(
  #       page_content="I had chocolate chip pancakes and scrambled eggs for breakfast this morning.",
  #       metadata={"source": "tweet"},
  #     ),
  #     Document(
  #       page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees.",
  #       metadata={"source": "news"},
  #     ),
  #   ]
      
  #   # Add documents to the store
  #   added_ids = qdrant_manager.add_documents(documents)
  #   # if self.debulogging.info(f"Added document IDs: {added_ids}")
    
  #   # Perform a similarity search
  #   search_results = qdrant_manager.search("LangChain provides abstractions to make working with LLMs easy", top_k=2)
  #   for res in search_results:
  #       logging.info(f"* {res.page_content} [{res.metadata}]")
  # except Exception as e:
  #   logging.critical(f"Error in main execution: {e}")
