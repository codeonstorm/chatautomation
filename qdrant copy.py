import os
from dotenv import load_dotenv
load_dotenv()  

from langchain_ollama import OllamaEmbeddings

from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

embeddings = OllamaEmbeddings(model="llama3")

QdrantClientUrl = os.getenv("QDRANT_CLIENT_URL")
QdrantClientApiKey = os.getenv("QDRANT_CLIENT_API_KEY")
qdrantClient = QdrantClient(url=QdrantClientUrl)

# On-disk storage:
# Local mode, without using the Qdrant server, may also store your vectors on disk so they persist between runs.
# qdrantClient = QdrantClient(path="/tmp/langchain_qdrant")

qdrantClient.create_collection(
    collection_name="demo_collection",
    vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
)

vector_store = QdrantVectorStore(
    client=qdrantClient,
    collection_name="demo_collection",
    embedding=embeddings
)

# Using an existing collection
qdrantClient = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="demo_collection",
    url=QdrantClientUrl
)


# Add items to vector store
from uuid import uuid4
from langchain_core.documents import Document

document_1 = Document(
    page_content="I had chocalate chip pancakes and scrambled eggs for breakfast this morning.",
    metadata={"source": "tweet"},
)

document_2 = Document(
    page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees.",
    metadata={"source": "news"},
)

documents = [
    document_1,
    document_2,
]
uuids = [str(uuid4()) for _ in range(len(documents))]

vector_store.add_documents(documents=documents, ids=uuids)



# Delete items from vector store
# vector_store.delete(ids=[uuids[-1]])


# Query vector store
# QdrantVectorStore supports 3 modes for similarity searches. They can be configured using the retrieval_mode parameter when setting up the class.

# -Dense Vector Search(Default)
# -Sparse Vector Search
# -Hybrid Search

results = vector_store.similarity_search(
    "LangChain provides abstractions to make working with LLMs easy", k=2
)
for res in results:
    print(f"* {res.page_content} [{res.metadata}]")



# url = "<---qdrant cloud cluster url here --->"
# api_key = "<---api key here--->"
# qdrant = QdrantVectorStore.from_documents(
#     docs,
#     embeddings,
#     url=url,
#     prefer_grpc=True,
#     api_key=api_key,
#     retrieval_mode=RetrievalMode.DENSE
#     collection_name="my_documents",
# )

# https://python.langchain.com/docs/integrations/vectorstores/qdrant/#local-mode