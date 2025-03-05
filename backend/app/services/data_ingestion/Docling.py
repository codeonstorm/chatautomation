# https://ds4sd.github.io/docling/examples/rag_langchain/#rag
from qdrant_client import QdrantClient
from qdrant_client.http import models
from docling.chunking import HybridChunker
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_docling.loader import ExportType
# from bs4 import BeautifulSoup
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import os
import sys
from uuid import uuid4

COLLECTION_NAME = "docling"
EXPORT_TYPE = ExportType.MARKDOWN
doc_converter = DocumentConverter(
  allowed_formats=[
    InputFormat.HTML, 
    # InputFormat.CSV, 
    # InputFormat.DOCX, 
    # InputFormat.PDF, 
    # InputFormat.MD,
    # InputFormat.PPTX, 
    # InputFormat.XLSX
  ]
)

# from langchain_community.document_loaders import BSHTMLLoader
# loader = BSHTMLLoader("https://www.5centscdn.net/blog/how-to-set-up-cdn-on-ecommerce-website/?pk_vid=6472d4f145978a631740846755a70b22")
# data = loader.load()
# print(data)


urls = ["https://www.5centscdn.net/blog/how-to-set-up-cdn-on-ecommerce-website/?pk_vid=6472d4f145978a631740846755a70b22"]
loader = UnstructuredURLLoader(urls=urls)
data = loader.load()

# soup = BeautifulSoup(data[0].page_content, "html.parser")
# clean_text = soup.get_text()
# print(data)

# Load the all-MiniLM-L6-v2 model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=500, chunk_overlap=100, separators=["\n\n", ".", " "]
)

chunked_docs = []
for doc in data:
  chunks = text_splitter.split_text(doc.page_content)
  for chunk in chunks:
    chunked_docs.append({
      "vector": embedding_model.encode(chunk),
      "payload": {
        "page_content": chunk,
        "metadata": doc.metadata
      }
    })

# Generate embeddings for all chunks
# chunk_embeddings = [embedding_model.encode(chunk["page_content"]) for chunk in chunked_docs]

client = QdrantClient(
  url=os.getenv("QDRANT_CLIENT_URL"),
  port=os.getenv("QDRANT_CLIENT_PORT"),
  api_key=os.getenv("QDRANT_CLIENT_API_KEY"),
  prefer_grpc=True
)

if not client.collection_exists(COLLECTION_NAME):
  client.create_collection(
    collection_name=COLLECTION_NAME,
    # vectors_config={ models.VectorParams(size=384, distance=models.Distance.COSINE)}
    vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)  # Adjust size if needed
  )

def upsert(client, collection_name: str, data) -> None:
  # Upload the vectors to the collection along with the original text as payload
  client.upsert(
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

# upsert(
#   client,
#   collection_name=COLLECTION_NAME,
#   data=chunked_docs
# )

# _ = client.add(
#   collection_name=COLLECTION_NAME,
#   documents=documents,
#   metadata=metadatas,
#   # batch_size=64,
# )

# points = client.query(
#   collection_name=COLLECTION_NAME,
#   query_text="how ecommerece helpfull?",
#   limit=10,
# )

# search_results = client.search(
#   collection_name=COLLECTION_NAME, 
#   query_vector=embedding_model.encode("How ecomerece help us"),
#   limit=10,
#   with_payload=True
# )

test = client.query_points(
  collection_name=COLLECTION_NAME, 
  query=embedding_model.encode("How ecomerece help us"),
  limit=10,
  with_payload=True
)

print(test)


# for i, point in enumerate(search_results):
#     print(f"=== {i} ===")
#     print(search_results.document)
#     print()













# client.set_model("sentence-transformers/all-MiniLM-L6-v2")
# client.set_sparse_model("Qdrant/bm25")

# source = "https://www.5centscdn.net/blog/how-to-set-up-cdn-on-ecommerce-website/?pk_vid=6472d4f145978a631740846755a70b22"  # document per local path or URL
# converter = DocumentConverter()
# result = converter.convert(source)
# docs = [result.document.export_to_markdown()]

# html_content = result.document.export_to_markdown()  # Assuming it's returning HTML-like content
# soup = BeautifulSoup(html_content, "html.parser")
# clean_text = soup.get_text()
 
# if EXPORT_TYPE == ExportType.DOC_CHUNKS:
#   splits = docs
# elif EXPORT_TYPE == ExportType.MARKDOWN:
#   splitter = MarkdownHeaderTextSplitter(
#     headers_to_split_on=[
#       ("#", "Header_1"),
#       ("##", "Header_2"),
#       ("###", "Header_3"),
#     ],
#   )
#   # splits = [split for doc in docs for split in splitter.split_text(doc.page_content)]
#   splits = []
#   for doc in docs:
#     text = getattr(doc, "page_content", doc)  # Get text safely
#     splits.extend(splitter.split_text(text))
# else:
#   raise ValueError(f"Unexpected export type: {EXPORT_TYPE}")
 
# documents, metadatas = [], []
# for chunk in HybridChunker().chunk(result.document):
#   documents.append(chunk.text)
#   # metadatas.append(chunk.meta.export_json_dict())
# print(documents[0])
# print("\n\n", metadatas)
