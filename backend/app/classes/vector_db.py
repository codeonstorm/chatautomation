from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, SearchParams
import uuid
import os
from dotenv import load_dotenv

load_dotenv()


class VectorDB:
    def __init__(self, collection_name="rag_docs"):
        """Initialize Qdrant Cloud connection."""
        self.host = os.getenv("QDRANT_CLIENT_URL", "")
        self.api_key = os.getenv("QDRANT_CLIENT_API_KEY", "")
        self.port = os.getenv("QDRANT_CLIENT_PORT", "")
        self.size = 384

        self.client = QdrantClient(
            url=self.host,
            api_key=self.api_key,
            port=self.port,
            prefer_grpc=True,
            timeout=5,
        )
        self.collection_name = collection_name
        self.create_collection()

    def create_collection(self):
        """Create collection in Qdrant if not exists."""
        existing_collections = self.client.get_collections().collections
        if self.collection_name not in [col.name for col in existing_collections]:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.size, distance=Distance.COSINE),
            )

    def insert_vector(self, embedding, text):
        """Insert a single embedding and associated text into Qdrant Cloud."""
        point = PointStruct(
            id=str(uuid.uuid4()), vector=embedding, payload={"text": text}
        )
        self.client.upsert(collection_name=self.collection_name, points=[point])

    def close(self):
        """Close Qdrant client connection."""
        self.client.close()

    # new 
    def search(self, query_vector, top_k=5):
        """Search for the most similar vectors in the collection."""
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            # score_threshold=0.5,
            search_params=SearchParams(hnsw_ef=128, exact=False)
        )
        return search_result



if __name__ == "__main__":
    vector_db = VectorDB()
