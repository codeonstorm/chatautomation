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
      tool for greeting query **only. example: Hi, Hello, Hey, Thanks, bye, OK, Good Morning, Good Evning.
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
          embedder = DocumentEmbedder()
          query_embedding = embedder.embedding_model.encode([user_query])[0]
          vectorDB = VectorDB('1-2b38345c-dda4-476a-bbd9-8724ea4f2851')
          results = vectorDB.search(query_embedding, top_k=5)

          # Extract matched texts and optional scores
          hits = [{"text": r.payload.get("text", ""), "score": r.score} for r in results]

          # print(hits)
          return hits
      except Exception as e:
          # return "At 5centsCDN, we are dedicated to delivering premium CDN services at competitive prices, starting from just 5 cents per GB. Our flexible approach means clients can engage with us without the need for long-term commitments or contracts, although we do have nominal setup fees for trial periods. We are proud to have expanded our client base to over 5000 diverse customers, including entities in OTT, IPTV, advertising, gaming, government and non-profit sectors, as well as major television channels.Our robust network features over 70 strategically placed Points of Presence (PoPs) around the globe, ensuring that our customers can easily connect to our standalone network. This expansive network setup minimizes latency, often directly within the ISP networks of end-users. By managing and operating our own network infrastructure, 5centsCDN guarantees a fast, secure, and cost-effective content delivery solution, effectively and reliably connecting your content to audiences worldwide"
          return f"Opps! Error during retrieving data {e}"


  