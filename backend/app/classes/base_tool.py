from app.classes.vector_db import VectorDB
from app.classes.document_embedding import DocumentEmbedder


class BaseTool:

    @staticmethod
    def clamp(value: float, min_value: float, max_value: float) -> float:
        """
        Clamps a value between a minimum and maximum value.
        """
        return max(min_value, min(max_value, value))

    @staticmethod
    def add_two_numbers(a: int, b: int) -> int:
        """
        Add two numbers

        Args:
          a (int): The first number
          b (int): The second number

        Returns:
          int: The sum of the two numbers
        """

        # The cast is necessary as returned tool call arguments don't always conform exactly to schema
        # E.g. this would prevent "what is 30 + 12" to produce '3012' instead of 42
        return int(a) + int(b)

    @staticmethod
    def subtract_two_numbers(a: int, b: int) -> int:
        """
        Subtract two numbers
        """

        # The cast is necessary as returned tool call arguments don't always conform exactly to schema
        return int(a) - int(b)

    @staticmethod
    def greeting(query: str) -> int:
        """
        tool for **only. example: Hi, Hello, Hey, Thanks, bye, OK, Good Morning, Good Evning.
          Args:
              query (str): The query
        Returns:
          (str): The result of the query
        """
        return query

    @staticmethod
    def retriever(user_query: str) -> str:
        """
        tool to get updated information for the user query.
        Args:
          user_query (str): The query string to search for relevant documents.
        Returns:
          (str): A list of dictionaries containing retrieved documents.
        """
        try:
            # qdrant_manager = QdrantManager()
            # vector_store = qdrant_manager.get_vector_store("chatbot")
            # retrieved_docs = vector_store.similarity_search(query, k=2)
            # return retrieved_docs
            print("user_query", user_query)
            embedder = DocumentEmbedder()
            query_embedding = embedder.embedding_model.encode([user_query])[0]
            vectorDB = VectorDB("2b38345c-dda4-476a-bbd9-8724ea4f2851")
            results = vectorDB.search(query_embedding, top_k=5)

            # Extract matched texts and optional scores
            hits = [
                {"text": r.payload.get("text", ""), "score": r.score} for r in results
            ]

            # print(hits)
            return hits
        except Exception as e:
            return f"Opps! Error during retrieving data {e}"
