from ollama import ChatResponse, chat, ResponseError, Client
from src.classes.QdrantManager import QdrantManager
# from ollama_python import ModelManagementAPI

final_response = chat(
  'llama3.2:1b-instruct-q3_K_L', 
  messages=,
)

print(f"{final_response.message.content}")