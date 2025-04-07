from langchain.text_splitter import RecursiveCharacterTextSplitter


class DocumentSplitter:
    def __init__(self, chunk_size=500, chunk_overlap=100):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def split_text(self, text):
        return self.splitter.split_text(text)  # Ensure this method exposes the functionality
