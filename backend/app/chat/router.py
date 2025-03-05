from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException, status
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

chat_router = APIRouter()

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
            user_message = data.get("message", "")
            
            # Simple echo bot response
            # In a real application, you would process the message and generate a response
            # This could involve calling an external API, using a language model, etc.
            response = f"You said: {user_message}"
            
            # Simulate thinking time
            await asyncio.sleep(1)
            
            await manager.send_personal_message(response, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

