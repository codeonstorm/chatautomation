from qdrant_client import QdrantClient, models
import ollama

COLLECTION_NAME = "NicheApplications"

# Initialize Ollama client
oclient = ollama.Client(host="localhost")

# Initialize Qdrant client
qclient = QdrantClient(host="localhost", port=6333)

# Text to embed
text = "Ollama excels in niche applications with specific embeddings"

# Generate embeddings
response = oclient.embeddings(model="llama3.2", prompt=text)
embeddings = response["embedding"]

# Create a collection if it doesn't already exist
if not qclient.collection_exists(COLLECTION_NAME):
    qclient.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=len(embeddings), distance=models.Distance.COSINE
        ),
    )

# Upload the vectors to the collection along with the original text as payload
qclient.upsert(
    collection_name=COLLECTION_NAME,
    points=[models.PointStruct(id=1, vector=embeddings, payload={"text": text})],
)