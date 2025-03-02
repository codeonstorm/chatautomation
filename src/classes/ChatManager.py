import ollama
from typing import Dict, List, Union

class ChatManager:

  _history: Dict[str, List[Dict[str, str]]] = {}

  def __init__(self, user_id: str) -> None:
    self.get_chat_history(self, user_id)
  
  def get_response(self, user_id: str, message: str, model: str = "mistral") -> str:
    if user_id not in self._history:
      self._history[user_id] = []
      
      # Append user message to history
      self._history[user_id].append({"role": "user", "content": message})
      
      # Generate response using Ollama API
      response: Dict[str, Union[str, Dict[str, str]]] = ollama.chat(model=model, messages=self._history[user_id])
      
      # Append AI response to history
      self._history[user_id].append({"role": "assistant", "content": response['message']['content']})
      
      return response['message']['content']
  
  def get_chat_history(self, user_id: str) -> List[Dict[str, str]]:
    """get last 3 chat history from db"""
    return self._history.get(user_id, [])
  
  def clear_chat_history(self, user_id: str) -> None:
    if user_id in self._history:
      del self._history[user_id]

# Example usage
if __name__ == "__main__":
  chat_manager = ChatManager()
  user_id: str = "user_123"
  
  print("User: Hello!")
  response: str = chat_manager.get_response(user_id, "Hello!")
  print(f"Assistant: {response}")
  
  print("User: How are you?")
  response = chat_manager.get_response(user_id, "How are you?")
  print(f"Assistant: {response}")
  
  print("Chat History:", chat_manager.get_chat_history(user_id))
  
  chat_manager.clear_chat_history(user_id)
  print("Chat history after clearing:", chat_manager.get_chat_history(user_id))
