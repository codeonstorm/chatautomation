import os

from typing import Iterator
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
# from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings, OllamaLLM, ChatOllama
from langchain_qdrant import QdrantVectorStore
from langchain_community.document_loaders import DirectoryLoader
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document as LCDocument
from langchain_docling import DoclingLoader
from docling.chunking import HybridChunker
from langchain_docling.loader import ExportType

from dotenv import load_dotenv
load_dotenv()

qdrant_url = os.getenv("QDRANT_CLIENT_URL")
qdrant_key = os.getenv("QDRANT_CLIENT_API_KEY")
qdrant_port = os.getenv("QDRANT_CLIENT_PORT")
EMBED_MODEL_ID = os.getenv("CHAT_MODEL")
EXPORT_TYPE = ExportType.MARKDOWN
FILE_PATH = "https://5centscdn.net"
            
llm = ChatOllama(  
    model = EMBED_MODEL_ID,  
    temperature = 0.8,  
    # num_predict = 256,  
    # other params ...  
)

# Create vector database
def create_vector_database():
    embedding = OllamaEmbeddings(model_name=EMBED_MODEL_ID)
    
    loader = DoclingLoader(
        file_path=FILE_PATH,
        export_type=EXPORT_TYPE,
        chunker=HybridChunker(tokenizer=embedding),
    )

    docling_documents = loader.load()
    
    # Determining the splits
    if EXPORT_TYPE == ExportType.DOC_CHUNKS:
        splits = docling_documents
    elif EXPORT_TYPE == ExportType.MARKDOWN:
        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header_1"),
                ("##", "Header_2"),
                ("###", "Header_3"),
            ],
        )
        splits = [split for doc in docling_documents for split in splitter.split_text(doc.page_content)]
    else:
        raise ValueError(f"Unexpected export type: {EXPORT_TYPE}")
    
    # print(splits)
    with open('data/output_docling.md', 'a') as f:  # Open the file in append mode ('a')
        for doc in docling_documents:
            f.write(doc.page_content + '\n')
    
    
    # # Initialize Embeddings
    # embedding = OllamaEmbeddings(model_name=EMBED_MODEL_ID)
    
    # # Create and persist a Qdrant vector database from the chunked documents
    # vectorstore = QdrantVectorStore.from_documents(
    #     documents=splits,
    #     embedding=embedding,
    #     url=qdrant_url,
    #     collection_name="rag",
    # )
    
    print('Vector DB created successfully !')


if __name__ == "__main__":
    create_vector_database()