import os
import json
import uvicorn
from fastapi import FastAPI, Request

# ----------------------------
# DOCUMENT PROCESSING CLASSES
# ----------------------------

from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np

class DocumentProcessor:
    def __init__(self, doc_dir: str, chunk_size: int = 500, overlap: int = 50):
        self.doc_dir = doc_dir
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.documents = []  # List of dicts with keys: filename, content
        self.chunks = []     # List of dicts with keys: filename, text, embedding

    def load_documents(self):
        for filename in os.listdir(self.doc_dir):
            if filename.endswith(".txt"):
                path = os.path.join(self.doc_dir, filename)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.documents.append({"filename": filename, "content": content})
        return self.documents

    def split_documents(self):
        splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.overlap)
        for doc in self.documents:
            chunks = splitter.split_text(doc["content"])
            for chunk in chunks:
                self.chunks.append({"filename": doc["filename"], "text": chunk})
        return self.chunks

    def compute_embeddings(self, model_name: str = "all-MiniLM-L6-v2"):
        model = SentenceTransformer(model_name)
        texts = [chunk["text"] for chunk in self.chunks]
        embeddings = model.encode(texts, convert_to_numpy=True)
        for i, chunk in enumerate(self.chunks):
            chunk["embedding"] = embeddings[i]
        return self.chunks

# ----------------------------
# QDRANT VECTOR DATABASE CLASS
# ----------------------------

from qdrant_client import QdrantClient

class QdrantManager:
    def __init__(self, collection_name: str = "chatbot_docs", vector_dim: int = 384):
        self.collection_name = collection_name
        self.vector_dim = vector_dim
        self.client = QdrantClient(":memory:")
        self._create_collection()

    def _create_collection(self):
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config={"size": self.vector_dim, "distance": "Cosine"}
        )

    def upsert_documents(self, chunks: list):
        points = []
        for idx, chunk in enumerate(chunks):
            point = {
                "id": idx,
                "vector": chunk["embedding"].tolist(),
                "payload": {"text": chunk["text"], "filename": chunk["filename"]}
            }
            points.append(point)
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query_vector: list, top_k: int = 3):
        return self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )

# ----------------------------
# LLM WRAPPER CLASS
# ----------------------------

class LLMWrapper:
    def __init__(self, model: str = "llama3.2:2b"):
        self.model = model

    def generate_response(self, prompt: str) -> str:
        import ollama  # Assumes the Ollama Python package is installed and configured
        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return response.get("message", {}).get("content", "")

# ----------------------------
# CHATBOT GRAPH (WORKFLOW) CLASS
# ----------------------------

class ChatbotGraph:
    def __init__(self, qdrant_manager: QdrantManager, llm_wrapper: LLMWrapper, query_embedding_model: SentenceTransformer):
        self.qdrant_manager = qdrant_manager
        self.llm_wrapper = llm_wrapper
        self.query_embedding_model = query_embedding_model

    def _embed_query(self, query: str) -> np.ndarray:
        return self.query_embedding_model.encode(query, convert_to_numpy=True)

    def get_context(self, query: str, top_k: int = 3) -> str:
        query_vector = self._embed_query(query)
        search_result = self.qdrant_manager.search(query_vector.tolist(), top_k=top_k)
        # Concatenate retrieved texts as context
        context = " ".join([res.payload["text"] for res in search_result])
        return context

    def run(self, query: str) -> str:
        context = self.get_context(query)
        prompt = (
            "Answer the following question based solely on the context provided.\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{query}\n\nAnswer:"
        )
        return self.llm_wrapper.generate_response(prompt)

# ----------------------------
# FASTAPI SERVICE CLASS
# ----------------------------

class ChatbotService:
    def __init__(self, chatbot_graph: ChatbotGraph):
        self.chatbot_graph = chatbot_graph
        self.app = FastAPI()
        self._setup_routes()

    def _setup_routes(self):
        @self.app.post("/chat")
        async def chat_endpoint(request: Request):
            data = await request.json()
            user_query = data.get("query", "")
            if not user_query:
                return {"error": "No query provided"}
            response_text = self.chatbot_graph.run(user_query)
            return {"response": response_text}

# ----------------------------
# MAIN APPLICATION INITIALIZATION
# ----------------------------

def main():
    # Step 1: Process documents
    DOC_DIR = "./documents"  # Ensure you have a folder named "documents" with .txt files
    doc_processor = DocumentProcessor(DOC_DIR)
    doc_processor.load_documents()
    doc_processor.split_documents()
    doc_processor.compute_embeddings()

    # Step 2: Initialize Qdrant and upload embeddings
    qdrant_mgr = QdrantManager(collection_name="chatbot_docs", vector_dim=384)
    qdrant_mgr.upsert_documents(doc_processor.chunks)

    # Step 3: Prepare the query embedding model (reuse SentenceTransformer)
    query_model = SentenceTransformer("all-MiniLM-L6-v2")

    # Step 4: Initialize LLM wrapper (calls local Llama3.2:2b via Ollama)
    llm_wrapper = LLMWrapper(model="llama3.2:2b")

    # Step 5: Build the chatbot graph (retrieval + prompt construction + LLM call)
    chatbot_graph = ChatbotGraph(qdrant_manager=qdrant_mgr, llm_wrapper=llm_wrapper, query_embedding_model=query_model)

    # Step 6: Create the FastAPI service with the chatbot graph
    chatbot_service = ChatbotService(chatbot_graph)

    # Launch the FastAPI server using uvicorn
    uvicorn.run(chatbot_service.app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
