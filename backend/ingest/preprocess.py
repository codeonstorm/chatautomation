from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import os


import sys
sys.exit()
# Temporary file storage path
UPLOAD_DIR = "../uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

file_names = os.listdir(UPLOAD_DIR)

print(file_names)

import sys
sys.exit()
# Load PDF
pdf_loader = PyPDFLoader("../uploads/DeepSeek_R1.pdf")
pdf_docs = pdf_loader.load()

# # Load DOCX
# docx_loader = Docx2txtLoader("sample.docx")
# docx_docs = docx_loader.load()

# # Load PPTX
# ppt_loader = UnstructuredPowerPointLoader("sample.pptx")
# ppt_docs = ppt_loader.load()

# Combine all documents
# all_docs = pdf_docs + docx_docs + ppt_docs
all_docs = pdf_docs


# Chunking documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(all_docs)

# Load Sentence Transformer Model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
chunk_texts = [chunk.page_content for chunk in chunks]
embeddings = embedding_model.encode(chunk_texts).tolist()

# print(embeddings)
