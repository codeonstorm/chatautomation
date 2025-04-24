from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
    status,
)
from fastapi.responses import HTMLResponse
from sqlmodel import Session
from typing import List
import asyncio
import json
from jose import JWTError, jwt
from pydantic import ValidationError

from app.core.auth import get_current_active_user
from app.core.config import settings
from app.core.database import get_session
from app.models.user import User
from app.schemas.token import TokenPayload
from uuid import UUID

from ollama import ChatResponse, chat, ResponseError, Client
import time
from app.classes.vector_db import VectorDB
from app.classes.document_embedding import DocumentEmbedder
from app.classes.base_tool import BaseTool
from app.classes.template import Template
from app.classes.greeting import GreetingResponder
from pathlib import Path

MODEL_DIR = Path("models")

chat_router = APIRouter(prefix="/chat/{chatbot_uuid}", tags=["chat"])
 
available_functions = {
    # 'greeting': greeting,
    "add_two_numbers": BaseTool.add_two_numbers,
    "subtract_two_numbers": BaseTool.subtract_two_numbers,
    "retriever": BaseTool.retriever,
}


# HTML template for the chat interface
html = """
<!DOCTYPE html>
<html>
<head>
    <title>BuyBot Chat</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            height: 100vh;
            background-color: #f5f5f5;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 100%;
            max-width: 800px;
            margin: 0 auto;
            width: 100%;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .header {
            background-color: #4a56e2;
            color: white;
            padding: 1rem;
            text-align: center;
            font-size: 1.5rem;
            font-weight: bold;
        }
        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            background-color: white;
        }
        .message {
            padding: 0.75rem 1rem;
            border-radius: 1rem;
            max-width: 80%;
            word-break: break-word;
        }
        .user {
            align-self: flex-end;
            background-color: #4a56e2;
            color: white;
            border-bottom-right-radius: 0.25rem;
        }
        .bot {
            align-self: flex-start;
            background-color: #e9e9eb;
            color: #333;
            border-bottom-left-radius: 0.25rem;
        }
        .input-container {
            display: flex;
            padding: 1rem;
            background-color: white;
            border-top: 1px solid #e0e0e0;
        }
        #messageText {
            flex: 1;
            padding: 0.75rem;
            border: 1px solid #e0e0e0;
            border-radius: 0.5rem;
            margin-right: 0.5rem;
            font-size: 1rem;
        }
        button {
            background-color: #4a56e2;
            color: white;
            border: none;
            border-radius: 0.5rem;
            padding: 0.75rem 1.5rem;
            cursor: pointer;
            font-size: 1rem;
            font-weight: bold;
        }
        button:hover {
            background-color: #3a46c2;
        }
        .auth-container {
            max-width: 400px;
            margin: 2rem auto;
            padding: 2rem;
            background-color: white;
            border-radius: 0.5rem;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .form-group {
            margin-bottom: 1rem;
        }
        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: bold;
        }
        input[type="email"], input[type="password"] {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #e0e0e0;
            border-radius: 0.5rem;
            font-size: 1rem;
        }
        .error-message {
            color: #e53935;
            margin-top: 1rem;
        }
        .typing-indicator {
            display: none;
            align-self: flex-start;
            background-color: #e9e9eb;
            color: #333;
            border-radius: 1rem;
            padding: 0.75rem 1rem;
            margin-top: 0.5rem;
        }
        .typing-indicator span {
            display: inline-block;
            width: 8px;
            height: 8px;
            background-color: #666;
            border-radius: 50%;
            animation: typing 1s infinite;
            margin-right: 3px;
        }
        .typing-indicator span:nth-child(2) {
            animation-delay: 0.2s;
        }
        .typing-indicator span:nth-child(3) {
            animation-delay: 0.4s;
        }
        @keyframes typing {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
    </style>
</head>
<body>
    <div id="chatContainer" class="chat-container">
        <div class="header">
            BuyBot
        </div>
        <div id="messages" class="messages">
            <div class="message bot">
                Hello! How can I help you today?
            </div>
        </div>
        <div id="typingIndicator" class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
        </div>
        <div class="input-container">
            <input type="text" id="messageText" placeholder="Type your message...">
            <button id="sendButton">Send</button>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script>
        let accessToken = '';
        let ws = null;

        connectWebSocket();

        function connectWebSocket() {
            // ws = new WebSocket(`ws://${window.location.host}/chat/ws?token=${accessToken}`);
            ws = new WebSocket(`ws://${window.location.host}/chat/${window.location.href.split('/')[4]}/ws?token=${accessToken}`);
            
            ws.onopen = function(event) {
                console.log('Connection opened');
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                addMessage(marked.parse(data.message), 'bot');
                document.getElementById('typingIndicator').style.display = 'none';
            };
            
            ws.onclose = function(event) {
                console.log('Connection closed');
                // Attempt to reconnect after a delay
                setTimeout(connectWebSocket, 3000);
            };
            
            ws.onerror = function(error) {
                console.error('WebSocket error:', error);
            };
        }

        document.getElementById('sendButton').addEventListener('click', sendMessage);
        document.getElementById('messageText').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        function sendMessage() {
            const messageInput = document.getElementById('messageText');
            const message = messageInput.value.trim();
            
            if (message && ws && ws.readyState === WebSocket.OPEN) {
                addMessage(message, 'user');
                ws.send(JSON.stringify({ message: message }));
                messageInput.value = '';
                
                // Show typing indicator
                document.getElementById('typingIndicator').style.display = 'block';
            }
        }

        function addMessage(message, sender) {
            const messagesContainer = document.getElementById('messages');
            const messageElement = document.createElement('div');
            messageElement.classList.add('message', sender);
            messageElement.innerHTML = message;
            messagesContainer.appendChild(messageElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    </script>
</body>
</html>
"""

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json({"message": message})


manager = ConnectionManager()


@chat_router.get("", response_class=HTMLResponse)
async def get_chat(
    chatbot_uuid: UUID
):
    # t1 = time.time()
    # from setfit import SetFitModel
    # model = SetFitModel.from_pretrained(MODEL_DIR / "buybot_setfit_model" / "buybot_setfit_model")
    # text = "I want to buy a new graphics card"
    # predictions = model([text])
    # print(f"===Prediction for '{text}': {predictions}", time.time() - t1)

    return HTMLResponse(content=html)


@chat_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, 
    chatbot_uuid: UUID,
    token: str = None
):
    """
    WebSocket endpoint for chat
    """
    from setfit import SetFitModel
    model = SetFitModel.from_pretrained(MODEL_DIR / "buybot_setfit_model" / "buybot_setfit_model")
    await manager.connect(websocket)
    chat_history_store = []
    try:
        while True:
            data = await websocket.receive_json()
            user_message_str = data.get("message", "")

            if not user_message_str:
                continue

            if len(user_message_str) < 2:
                await manager.send_personal_message("Hello! How can I help you today?", websocket)
                continue

            responder = GreetingResponder()
            response = responder.check_greeting(user_message_str)

            if response:
                await manager.send_personal_message(response, websocket)
                continue

            t1 = time.time()
            predictions = model([user_message_str])
            print(f"===SetFitModel '{user_message_str}': {predictions}", time.time() - t1)
            
            start_time = time.time()
            try:
                stand = [
                        Template.condense_question_system_template(),                    
                    ]
                for v in chat_history_store:
                    stand.append(v)
                stand.append({"role": "user", "content": user_message_str})

                print('\n\n stand: ', stand)
                standaloneresponse: ChatResponse = chat(
                    "gemma3:1b",
                    keep_alive="60m",
                    messages=stand
                )
            except ResponseError as e:
                print("Error:", e.error)
                await manager.send_personal_message("Error...S", websocket)
                continue
        
            print("\n\n gemma3:1b stanalone: ", standaloneresponse.message.content, time.time() - start_time)
            user_message = {"role": "user", "content": standaloneresponse.message.content}
            chat_history_store.append({
                "role": "user",
                "content": user_message_str,
            })
            print("\n\Question:", user_message["content"])

            # Call the model with tools
            tool_prompt = []
            tool_prompt.append(Template.system_prompt_for_tools_intro())
            tool_prompt.extend(chat_history_store)

            try:
                t2 = time.time()
                response: ChatResponse = chat(
                    "llama3.2:1b-instruct-q3_K_L",
                    keep_alive="60m",
                    messages=tool_prompt,
                    tools=[BaseTool.greeting, BaseTool.add_two_numbers, BaseTool.subtract_two_numbers, BaseTool.retriever],
                )
                print("===Tool response time:", time.time() - t2)
            except ResponseError as e:
                print("Error:", e.error)
                await manager.send_personal_message("Error...S", websocket)
                continue

            print("\n\nSelected:", response, end="\n\n")

            messages = [Template.system_prompt_for_output(), user_message]
            if response.message.tool_calls:
                tool_outputs = []
                for tool_call in response.message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = tool_call.function.arguments
                    # function_args = {k: int(v) for k, v in function_args.items()}

                    if function_to_call := available_functions.get(function_name):
                        print(
                            "\n\n == Calling function: ==",
                            function_name,
                            "Arguments:",
                            function_args,
                            end="\n\n",
                        )

                        if function_name != "greeting":
                            # if function_name != 'retriver':
                            result = function_to_call(**function_args)
                            tool_outputs.append(
                                {
                                    "role": "tool",
                                    "name": function_name,
                                    "content": str(result),
                                }
                            )

                if tool_outputs:
                    messages.extend(tool_outputs)

                print("\n\n **Tool used:\n", function_name, end="\n\n")
                print("\n\n **Final Messages:\n", messages, end="\n\n")

            # Get final response
            try:
                final_response = chat(
                    "llama3.2:1b-instruct-q3_K_L",
                    messages=messages,
                    keep_alive="60m",
                )

                chat_history_store.append({
                    "role": "assistant",
                    "content": final_response.message.content,
                })
            except ResponseError as e:          
                print("Error:", e.error)
                await manager.send_personal_message("Error...S", websocket)
                continue

            print("\n\n\n history:", chat_history_store)
            # print("\n\nFinal response:\n", final_response.message.content)

            # for chunk in final_response:
            #   await websocket.send_text(f"{chunk['message']['content']}")
            #   print(chunk['message']['content'], end='', flush=True)

            end_time = time.time()
            elapsed_time = end_time - start_time
            await manager.send_personal_message(final_response.message.content + ' **time take:' + str(round(elapsed_time)) +  ' second' , websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
