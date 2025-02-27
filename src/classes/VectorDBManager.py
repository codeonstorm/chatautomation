from typing import Any, Dict, List, Optional, Union, Sequence
from qdrant_client import QdrantClient
from qdrant_client.http import models
import logging
from langchain_ollama import OllamaEmbeddings
from uuid import uuid4


# Define the type for a point in Qdrant.
PointType = Dict[str, Any]  # expects keys: "id", "vector", optional "payload"

class VectorDBManager:
  """
  Parameters:
    host (str): Qdrant host address (default 'localhost').
    port (int): Qdrant port (default 6333).
    collection_name (str): Name of the collection to use.
    vector_size (int): Dimension of the vectors.
    distance (str): Distance metric: 'Cosine', 'Euclidean', or 'Dot' (default 'Cosine').
  """
  def __init__(
    self,
    host: str,
    port: int,
    api_key: str,
    collection_name: str,
    vector_size: int,
    distance: str = models.Distance.COSINE
  ) -> None:
    self.collection_name: str = collection_name
    self.vector_size: int = vector_size
    self.distance: str = distance
    
    # Initialize Qdrant client.
    self.client: QdrantClient = QdrantClient(url=host, port=port, api_key=api_key, prefer_grpc=True)
    self.create_collection(self.collection_name)

  def get_client(self) -> QdrantClient:
    return self.client
  
  def create_collection(self, collection_name: str) -> bool:
    """
    Create a new collection in Qdrant.
    """
    try:
      if not self.client.collection_exists(self.collection_name):
        self.client.create_collection(
          collection_name=self.collection_name,
          vectors_config=models.VectorParams(size=self.vector_size, distance=self.distance),
        )
        logging.info(f"New collection {collection_name} created successfully.")
      return True
    except Exception as e:
      raise ValueError(f"Error creating collection: {e}")

  def delete_collection(self, collection_name: str) -> bool:
    """
    Delete a collection in Qdrant.
    """
    try:
      if self.client.collection_exists(collection_name):
        self.client.delete_collection(collection_name)
        logging.info(f"Collection {collection_name} deleted successfully.")
      return True
    except Exception as e:
      logging.error(f"Error deleting collection: {e}")
      return False
 
  def get_collections(self) -> List[str]:
    """
    Get a list of collections in Qdrant.
    """
    try:
      return self.client.get_collections()
    except Exception as e:
      logging.error(f"Error getting collections: {e}")
      return []
  
  def upsert(self, collection_name: str, data: List[Dict[Any, Any]]) -> None:
    # Upload the vectors to the collection along with the original text as payload
    self.client.upsert(
      collection_name=collection_name,
      points=[
        models.PointStruct(
          id=str(uuid4()),
          vector=row["vector"],
          payload=row["payload"]
        )
        for row in data
      ]
    )

  def search(
    self, 
    collection_name: str,
    query_vector: Any,
    limit: int = 5,
    with_payload: bool = True,
  ) -> List[Any]: 
    """
    Search for the nearest vectors to a given query vector.
    """
    try:
      search_results = self.client.search(
        collection_name=collection_name, 
        query_vector=query_vector,
        limit=limit,
        with_payload=with_payload
      )
      return search_results
    except Exception as e:
      logging.error(f"Error searching vectors: {e}")
      return []

  def close_connection(self) -> None:
    """
    Close the connection to Qdrant.
    """
    self.client.close()



if __name__ == "__main__":

  from dotenv import load_dotenv
  import os

  load_dotenv()

  qdrant_db = VectorDBManager(
    host=os.getenv("QDRANT_CLIENT_URL"),
    port=os.getenv("QDRANT_CLIENT_PORT"),
    api_key=os.getenv("QDRANT_CLIENT_API_KEY"),
    collection_name="test", 
    vector_size=128, 
    distance=models.Distance.COSINE
  )

  # import random
  # qdrant_db.upsert(
  #   collection_name="test",
  #   data=[{
  #     "vector": [0.15] * 128,
  #     "payload": {"content": "red", "metadata": {
  #       "name": "John Doe",
  #       "age": 30,
  #     }}
  #   }]
  # )


  # Search for the nearest vectors to a given query vector.
  # query: List[float] = [0.15] * 128
  # search_results = qdrant_db.search(collection_name="test", query_vector=query, limit=2)
  # print("Search Results:")
  # for result in search_results:
  #   print(result)
  
  # # Delete a point by id.
  # delete_result = qdrant_db.delete_point(2)
  # print("Delete Result:", delete_result)