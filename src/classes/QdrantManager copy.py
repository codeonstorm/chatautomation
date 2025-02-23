import os
import logging
# from dotenv import load_dotenv
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
    logging.FileHandler("../../logs/qdrant_manager.log"),
    logging.StreamHandler()
  ]
)

class QdrantManager:
  client = None  #static variable
  
  def __init__(self, vector_size=3072, distance_metric=Distance.COSINE, model_name="llama3.2"):
    """Initialize the QdrantManager with collection configuration."""
    try:
      # load_dotenv()
      self.qdrant_url = os.getenv("QDRANT_CLIENT_URL")
      self.qdrant_api_key = os.getenv("QDRANT_CLIENT_API_KEY")
      self.debug = os.getenv("DEBUG", False)
      self.vector_store = {}  # Lazy initialization
      
      if not self.qdrant_url or not self.qdrant_api_key:
        raise ValueError("Missing Qdrant configuration in environment variables.")
      
      self.embeddings = OllamaEmbeddings(model=model_name)
      QdrantManager.client = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key)

    except Exception as e:
      logging.error(f"Error initializing QdrantManager: {e}")
      raise

  def get_vector_store(self, collection_name="chatbot"):
    """Get the Qdrant vector store."""
    try:
      self._initialize_vector_store(collection_name)
      return self.vector_store
    except Exception as e:
      logging.error(f"Error getting vector store: {e}")
      return

  # def _initialize_collection(self, vector_size, distance_metric):
  #   """Create a collection in Qdrant if it doesn't exist."""
  #   try:
  #     self.client.create_collection(
  #       collection_name=self.collection_name,
  #       vectors_config=VectorParams(size=vector_size, distance=distance_metric),
  #       )
  #   except Exception as e:
  #     logging.warning(f"Error initializing collection: {e}")

  def _initialize_vector_store(self, collection_name):
    """Lazy initialization of vector store."""
    if self.vector_store.collection_name is not QdrantVectorStore:
      self.vector_store.collection_name = QdrantVectorStore.from_existing_collection(
        embedding=OllamaEmbeddings(model="llama3.2"),
        collection_name=collection_name,
        prefer_grpc=True,
        url=self.qdrant_url,
        api_key=self.qdrant_api_key,
      )

  # def add_documents(self, documents):
  #   """Add documents to the Qdrant vector store."""
  #   try:
  #     self._initialize_vector_store()
  #     uuids = [str(uuid4()) for _ in range(len(documents))]
  #     self.vector_store.add_documents(documents=documents, ids=uuids)
  #     if self.debug: logging.info("Documents added successfully.")
  #     return uuids
  #   except Exception as e:
  #     logging.error(f"Error adding documents: {e}")
  #     return []

  # def delete_documents(self, doc_ids):
  #   """Delete documents from the Qdrant vector store."""
  #   try:
  #     self._initialize_vector_store()
  #     self.vector_store.delete(ids=doc_ids)
  #     if self.debug: logging.info("Documents deleted successfully.")
  #   except Exception as e:
  #     logging.error(f"Error deleting documents: {e}")

  # def search(self, query, top_k=2):
    """Perform a similarity search in the vector store."""
    try:
      self._initialize_vector_store()
      results = self.vector_store.similarity_search(query, k=top_k)
      if self.debug: logging.info("Search executed successfully.")
      return results
    except Exception as e:
      logging.error(f"Error performing search: {e}")
      return []

  def create_new_collection(self, collection_name, vector_size=3072, distance_metric=Distance.COSINE):
    """Create a new collection in Qdrant."""
    
    try:
      QdrantManager.client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=distance_metric),
      )
      if self.debug: logging.info(f"Collection {collection_name} created successfully.")
      self.vector_store = None  # Reset vector store
    except Exception as e:
      logging.error(f"Error creating collection: {e}")


# Usage Example
if __name__ == "__main__":
  qdrant_manager = QdrantManager()

  # client = QdrantClient(
  #   url="https://84b95ad8-91ed-4af2-baf0-5dba0aa656c6.us-east4-0.gcp.cloud.qdrant.io:6333", 
  #   api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.m-UBqSi16YI_9GG0Blo28rls04LW3qvYm26yKlMTVjk",
  #   prefer_grpc=True,
  # )

  # if not client.collection_exists("chatbot"):
  #   logging.error(f"Error chatbot collection not exists")
    # client.create_collection(
    # collection_name="startups",
    # vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    # )


  # print(qdrant_client.get_collections())

  # docs = []  
  # qdrant = QdrantVectorStore.from_documents(
  #   docs,
  #   embedding=OllamaEmbeddings(model="llama3.2"),
  #   url="https://84b95ad8-91ed-4af2-baf0-5dba0aa656c6.us-east4-0.gcp.cloud.qdrant.io:6333",
  #   prefer_grpc=True,
  #   api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.m-UBqSi16YI_9GG0Blo28rls04LW3qvYm26yKlMTVjk",
  #   collection_name="chatbot",
  # )

  # print("===", qdrant)

  # vector_store = QdrantVectorStore.from_existing_collection(
  #   embedding=OllamaEmbeddings(model="llama3.2"),
  #   collection_name="chatbot",
  #   prefer_grpc=True,
  #   url="https://84b95ad8-91ed-4af2-baf0-5dba0aa656c6.us-east4-0.gcp.cloud.qdrant.io:6334",
  #   api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.m-UBqSi16YI_9GG0Blo28rls04LW3qvYm26yKlMTVjk",
  # )

  # print("yy", qdrant)

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

  # retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 2})
  # data = retriever.invoke("Stealing from the bank is a crime")
  # print(data)


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
