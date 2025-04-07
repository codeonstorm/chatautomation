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

from ollama import ChatResponse, chat, ResponseError, Client
import time

chat_router = APIRouter()

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


def subtract_two_numbers(a: int, b: int) -> int:
    """
    Subtract two numbers
    """

    # The cast is necessary as returned tool call arguments don't always conform exactly to schema
    return int(a) - int(b)


def greeting(query: str) -> int:
    """
    tool for greeting query **only. example: Hi, Hello, Hey, Thanks, bye, OK, Good Morning, Good Evning.
      Args:
          query (str): The query
    Returns:
      (str): The result of the query
    """
    return query


def retriver(user_query: str) -> str:
    """
    tool to get updated information for the user query.
    Args:
      user_query (str): The query string to search for relevant documents.
    Returns:
      (str): A list of dictionaries containing retrieved documents.
    """
    try:
        qdrant_manager = QdrantManager()
        vector_store = qdrant_manager.get_vector_store("chatbot")
        retrieved_docs = vector_store.similarity_search(query, k=2)
        return retrieved_docs
    except Exception as e:
        print("==========")
        return "At 5centsCDN, we are dedicated to delivering premium CDN services at competitive prices, starting from just 5 cents per GB. Our flexible approach means clients can engage with us without the need for long-term commitments or contracts, although we do have nominal setup fees for trial periods. We are proud to have expanded our client base to over 5000 diverse customers, including entities in OTT, IPTV, advertising, gaming, government and non-profit sectors, as well as major television channels.Our robust network features over 70 strategically placed Points of Presence (PoPs) around the globe, ensuring that our customers can easily connect to our standalone network. This expansive network setup minimizes latency, often directly within the ISP networks of end-users. By managing and operating our own network infrastructure, 5centsCDN guarantees a fast, secure, and cost-effective content delivery solution, effectively and reliably connecting your content to audiences worldwide"
        return f"Opps! Error during retrieving data {e}"


available_functions = {
    # 'greeting': greeting,
    "add_two_numbers": add_two_numbers,
    "subtract_two_numbers": subtract_two_numbers,
    "retriver": retriver,
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
    <div id="authContainer" class="auth-container">
        <h2>Login to Chat</h2>
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" placeholder="Enter your email">
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" placeholder="Enter your password">
        </div>
        <button id="loginButton">Login</button>
        <div id="errorMessage" class="error-message"></div>
    </div>

    <div id="chatContainer" class="chat-container" style="display: none;">
        <div class="header">
            FastAPI Chat
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

    <script>
        let accessToken = '';
        let ws = null;

        document.getElementById('loginButton').addEventListener('click', async () => {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            if (!email || !password) {
                document.getElementById('errorMessage').textContent = 'Please enter both email and password';
                return;
            }
            
            try {
                const response = await fetch('/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({
                        'username': email,
                        'password': password,
                    }),
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    accessToken = data.access_token;
                    document.getElementById('authContainer').style.display = 'none';
                    document.getElementById('chatContainer').style.display = 'flex';
                    connectWebSocket();
                } else {
                    document.getElementById('errorMessage').textContent = data.detail || 'Login failed';
                }
            } catch (error) {
                document.getElementById('errorMessage').textContent = 'An error occurred. Please try again.';
                console.error('Login error:', error);
            }
        });

        function connectWebSocket() {
            ws = new WebSocket(`ws://${window.location.host}/chat/ws?token=${accessToken}`);
            
            ws.onopen = function(event) {
                console.log('Connection opened');
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                addMessage(data.message, 'bot');
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
            messageElement.textContent = message;
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


@chat_router.get("/chat", response_class=HTMLResponse)
async def get_chat():
    """
    Get the chat UI
    """
    return HTMLResponse(content=html)


@chat_router.websocket("/chat/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = None):
    """
    WebSocket endpoint for chat
    """
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        # Verify token (simplified for example)
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if token_data.type != "access":
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
    except (JWTError, ValidationError):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            user_message_str = data.get("message", "")
            if not user_message_str:
                continue
            start_time = time.time()
            # User message
            system_prompt = {
                "role": "system",
                "content": "You are an 5centsCDN AI chatbot always use provided tools and formats responses in Markdown with maximum 180 words",
            }  #
            # system_prompt_tool = {"role": "system", "content": "You are an AI assistant. If multiple tools are available, you MUST select only the most relevant ONE. Do NOT select multiple tools at once."} #
            user_message = {"role": "user", "content": user_message_str}
            # toos_msg = {'role': 'tool', 'content': "At 5centsCDN, we are dedicated to delivering premium CDN services at competitive prices, starting from just 5 cents per GB. Our flexible approach means clients can engage with us without the need for long-term commitments or contracts, although we do have nominal setup fees for trial periods. We are proud to have expanded our client base to over 5000 diverse customers, including entities in OTT, IPTV, advertising, gaming, government and non-profit sectors, as well as major television channels.Our robust network features over 70 strategically placed Points of Presence (PoPs) around the globe, ensuring that our customers can easily connect to our standalone network. This expansive network setup minimizes latency, often directly within the ISP networks of end-users. By managing and operating our own network infrastructure, 5centsCDN guarantees a fast, secure, and cost-effective content delivery solution, effectively and reliably connecting your content to audiences worldwide"}
            print("\n\nPrompt:", user_message["content"])

            # Prepare messages
            messages = [system_prompt, user_message]

            # Call the model with tools
            try:
                response: ChatResponse = chat(
                    "llama3.2:1b-instruct-q3_K_L",
                    messages=messages,
                    tools=[greeting, add_two_numbers, subtract_two_numbers, retriver],
                )
            except ResponseError as e:
                print("Error:", e.error)

            print("\n\nSelected:", response, end="\n\n")

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
                            print("\n\nFunction output:", result, end="\n\n")
                            tool_outputs.append(
                                {
                                    "role": "tool",
                                    "name": function_name,
                                    "content": str(result),
                                }
                            )

                if tool_outputs:
                    # Append tool outputs correctly
                    messages.extend(tool_outputs)
                    # Explicitly instruct the model to respond based on the tool results
                    # messages.append({'role': 'user', 'content': 'What is the final answer?'})
                    # messages.append({'role': 'system', 'content': "Use the provided context of information to answer the question."})
                    # messages.append({"role": "system", "content": "You are an AI chatbot always formats responses in Markdown."})

                print("\n\n **Final Messages:\n", messages, end="\n\n")

                # Get final response
            try:
                final_response = chat(
                    "llama3.2:1b-instruct-q3_K_L",
                    messages=messages,
                    keep_alive="50m",
                )
            except ResponseError as e:
                print("Error:", e.error)

            print("\n\nFinal response:\n", final_response.message.content)

            # for chunk in final_response:
            #   await websocket.send_text(f"{chunk['message']['content']}")
            #   print(chunk['message']['content'], end='', flush=True)

            end_time = time.time()
            elapsed_time = end_time - start_time
            await manager.send_personal_message(final_response.message.content, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
