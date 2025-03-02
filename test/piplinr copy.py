from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
import docling

# Step 1: Load documents
def load_documents(directory: str):
    loader = DirectoryLoader(directory, glob='*.txt')  # Adjust for PDFs, CSVs, etc.
    documents = loader.load()
    return documents

# Step 2: Preprocess & Chunk documents
def preprocess_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    return chunks

# Step 3: Embed and Store
vector_store_path = "faiss_index"
def embed_and_store(chunks):
    embeddings = OllamaEmbeddings(model_name="mistral")  # Adjust model as needed
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(vector_store_path)
    return vector_store

# Step 4: Query Processing
def query_rag(query: str):
    embeddings = OllamaEmbeddings(model_name="mistral")
    vector_store = FAISS.load_local(vector_store_path, embeddings)
    retriever = vector_store.as_retriever()
    llm = Ollama(model="mistral")
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)
    return qa_chain.run(query)

# Pipeline Execution
docs = load_documents("./data")
chunks = preprocess_documents(docs)
vector_store = embed_and_store(chunks)
response = query_rag("What is in the documents?")
print(response)
