from dotenv import load_dotenv
import os

os.environ["USER_AGENT"] = "MyCustomUserAgent"
# Load environment variables
load_dotenv()

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from src.classes.ChatbotPipeline import ChatbotPipeline

app = FastAPI()
chatbot = ChatbotPipeline()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>wisdom Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         res = chatbot.run(data)
#         await websocket.send_text(f"Message text was: {res}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await chatbot.websocket_handler(websocket)
