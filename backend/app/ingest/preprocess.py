import logging
import requests
import uuid
import os
from pathlib import Path
from bs4 import BeautifulSoup
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredPowerPointLoader,
    Docx2txtLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from app.classes.file_helper import FileHelper
from app.classes.vector_db import VectorDB

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DocumentProcessor:
    def __init__(self):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=100
        )
        self.vector_db = VectorDB()

    def get_loader(self, file):
        """Returns the appropriate document loader based on file extension."""
        ext = file.get("extension")
        file_path = self.upload_dir / file.get("name")
        if ext == ".pdf":
            return PyPDFLoader(file_path)
        elif ext == ".docx":
            return Docx2txtLoader(file_path)
        elif ext == ".pptx":
            return UnstructuredPowerPointLoader(file_path)
        else:
            return None

    def process_documents(self, upload_dir: Path):
        """Processes documents by extracting text, generating embeddings, and uploading them one by one."""
        self.upload_dir = upload_dir
        self.files = FileHelper(self.upload_dir).get_file_details()

        for file in self.files:
            loader = self.get_loader(file)
            if not loader:
                logging.warning(f"Skipping unsupported file type: {file.get('name')}")
                continue

            try:
                docs = loader.lazy_load()
                chunks = self.text_splitter.split_documents(docs)
                for chunk in chunks:
                    embedding = self.embedding_model.encode(chunk.page_content).tolist()
                    self.vector_db.insert_vector(embedding, chunk.page_content)
                logging.info(
                    f"Processed file: {file.get('name')}, Chunks: {len(chunks)}"
                )
            except Exception as e:
                logging.error(f"Error processing {file.get('name')}: {e}")

    def process_webpage(self, url: str):
        """Fetches webpage content, extracts text, generates embeddings, and uploads them one by one."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            texts = [p.get_text() for p in soup.find_all("p")]
            webpage_text = " ".join(texts)

            if not webpage_text:
                logging.warning(f"No extractable text found at {url}")
                return None

            chunks = self.text_splitter.split_text(webpage_text)
            for chunk in chunks:
                embedding = self.embedding_model.encode(chunk).tolist()
                self.vector_db.insert_vector(embedding, chunk)
            logging.info(f"Processed webpage: {url}, Chunks: {len(chunks)}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching webpage {url}: {e}")
            return None


if __name__ == "__main__":
    UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads" / "1"
    processor = DocumentProcessor()
    processor.process_documents(UPLOAD_DIR)

    # Uncomment to process a webpage
    processor.process_webpage("http://example.com")
    processor.vector_db.close()
