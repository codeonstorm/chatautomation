from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from langchain.llms import Ollama
from langgraph.graph import Graph
import asyncio

# Initialize FastAPI app
app = FastAPI()

llm = Ollama(model="llama3.2") 

# Define a LangGraph-based chat bot
class LangGraphChatBot:
    def __init__(self):
        self.graph = Graph()
        self.graph.add_node("llm", self.llm_response)
        self.graph.set_entry_point("llm")
        self.executor = self.graph.compile()

    async def llm_response(self, input_text):
        async for chunk in llm.astream(input_text):
            yield chunk  # Stream response chunks

    async def stream_responses(self, prompt):
        async for chunk in self.executor.invoke(prompt):
            yield chunk

# Initialize chatbot instance
chatbot = LangGraphChatBot()

# WebSocket endpoint
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            prompt = await websocket.receive_text()
            async for response in chatbot.stream_responses(prompt):
                await websocket.send_text(response)
    except WebSocketDisconnect:
        print("Client disconnected")
