from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer


class DocumentEmbedder:
    def __init__(self):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=100
        )


from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer


class DocumentEmbedder:
    def __init__(self, chunk_size=500, chunk_overlap=100, model_name="all-MiniLM-L6-v2"):
        self.embedding_model = SentenceTransformer(model_name)
        # self.text_splitter = RecursiveCharacterTextSplitter(
        #     chunk_size=chunk_size, chunk_overlap=chunk_overlap
        # )

    def embed_text(self, text):
        """Splits the text and returns embeddings for each chunk."""
        # chunks = self.text_splitter.split_text(text)
        # embeddings = self.embedding_model.encode(chunks, convert_to_tensor=True)
        # return list(zip(chunks, embeddings))
