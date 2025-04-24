from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
    status,
    Request
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
from setfit import SetFitModel

from sqlmodel import Session, select
from app.core.database import get_session
from app.models.chatbot import Chatbot

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

MODEL_DIR = Path("models")
model = SetFitModel.from_pretrained(MODEL_DIR / "buybot_setfit_model" / "buybot_setfit_model")

chat_router = APIRouter(prefix="/chat/{chatbot_uuid}", tags=["chat"])
templates = Jinja2Templates(directory="templates")
 
available_functions = {
    # 'greeting': greeting,
    "add_two_numbers": BaseTool.add_two_numbers,
    "subtract_two_numbers": BaseTool.subtract_two_numbers,
    "retriever": BaseTool.retriever,
}

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
    request: Request,
    chatbot_uuid: UUID,
    session: Session = Depends(get_session)
):
    try:
        chatbot = session.exec(
            select(Chatbot).where(Chatbot.uuid == chatbot_uuid)
        ).first()
    except Exception as e:
        print("Error fetching chatbot:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    if not chatbot:
     return HTMLResponse(status_code=404, content="Chatbot not found")

    return templates.TemplateResponse("chatbot.html", {
        "request": request,
        "chatbot": chatbot
    })


@chat_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, 
    chatbot_uuid: UUID,
    token: str = None
):
    """
    WebSocket endpoint for chat
    """
    await manager.connect(websocket)
    chat_history_store = []
    try:
        while True:
            data = await websocket.receive_json()
            start_time = time.time()
            user_message_str = data.get("message", "")
            standalone_question = ""

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
            
            try:
                t1 = time.time()
                predicted_intent = model([user_message_str])
                print(f"\n\n\n\nSetFitModel Intent ': {predicted_intent} {time.time() - t1} seconds")

                if predicted_intent == 'greeting':
                    await manager.send_personal_message("Hello! How can I help you today?", websocket)
                    continue
                elif predicted_intent == 'goodbye':
                    await manager.send_personal_message("Take care, until next time!", websocket)
                    continue
                elif predicted_intent == 'restricted_content':
                    await manager.send_personal_message("I'm here to help with respectful, safe, and appropriate topics. Let's keep things positive and productive!", websocket)
                    continue
                elif predicted_intent == 'schedule_meet':
                    await manager.send_personal_message("Sorry, I don't have enough information to schedule meeting", websocket)
                    continue
                
                # Standalone Question Preparation
                stand = [Template.condense_question_system_template()]
                for history in chat_history_store:
                    stand.append(history)
                stand.append({"role": "user", "content": user_message_str})
                # print('\n\n stand: ', stand)

                t2 = time.time()
                standalone_response: ChatResponse = chat(
                    # "gemma3:1b",
                    "llama3.2:1b-instruct-q3_K_L",
                    keep_alive="60m",
                    messages=stand
                )
                standalone_question = standalone_response.message.content
                print("\ngemma3:1b stanalone Que: ", standalone_question, time.time() - t2, 'seconds')

            except ResponseError as e:
                print("Error:", e.error)
                await manager.send_personal_message("Error...", websocket)
                continue
        
            # Update chat history with the standalone question
            user_message = {"role": "user", "content": standalone_question}
            chat_history_store.append({
                "role": "user",
                "content": user_message_str,
            })

            # ////////////// tool calls ////////////////

            # Call the model with tools
            # tool_prompt = []
            # tool_prompt.append(Template.system_prompt_for_tools_intro())
            # tool_prompt.extend(chat_history_store)

            # try:
            #     t3 = time.time()
            #     response: ChatResponse = chat(
            #         "llama3.2:1b-instruct-q3_K_L",
            #         keep_alive="60m",
            #         messages=tool_prompt,
            #         tools=[BaseTool.greeting, BaseTool.add_two_numbers, BaseTool.subtract_two_numbers, BaseTool.retriever],
            #     )
            #     print("===Tool response time:", time.time() - t3)
            # except ResponseError as e:
            #     print("Error:", e.error)
            #     await manager.send_personal_message("Error...S", websocket)
            #     continue

            # print("\n\nSelected:", response, end="\n\n")

            # messages = [Template.system_prompt_for_output(), user_message]
            # if response.message.tool_calls:
            #     tool_outputs = []
            #     for tool_call in response.message.tool_calls:
            #         function_name = tool_call.function.name
            #         function_args = tool_call.function.arguments
            #         # function_args = {k: int(v) for k, v in function_args.items()}

            #         if function_to_call := available_functions.get(function_name):
            #             print(
            #                 "\n\n == Calling function: ==",
            #                 function_name,
            #                 "Arguments:",
            #                 function_args,
            #                 end="\n\n",
            #             )

            #             if function_name != "greeting":
            #                 # if function_name != 'retriver':
            #                 result = function_to_call(**function_args)
            #                 tool_outputs.append(
            #                     {
            #                         "role": "tool",
            #                         "name": function_name,
            #                         "content": str(result),
            #                     }
            #                 )

            #     if tool_outputs:
            #         messages.extend(tool_outputs)

            #     print("\n\n **Tool used:\n", function_name, end="\n\n")
            #     print("\n\n **Final Messages:\n", messages, end="\n\n")

                # ////////////// tool calls ////////////////

            # Get final response
            t3 = time.time()
            tool_response = BaseTool.retriever(standalone_question)
            print("\n===Tool response time:", time.time() - t3, 'seconds\n')
            print("Tool response:\n", tool_response, end="\n\n")
            tool_message = {
                "role": "tool",
                "name": 'retriever',
                "content": str(tool_response),
            }
            messages = [Template.system_prompt_for_output(), tool_message, user_message]
            try:
                t4 = time.time()
                final_response = chat(
                    "llama3.2:1b-instruct-q3_K_L",
                    messages=messages,
                    keep_alive="60m",
                )
                print("===LLAMA response time:", time.time() - t4, 'seconds')

                chat_history_store.append({
                    "role": "assistant",
                    "content": final_response.message.content,
                })
            except ResponseError as e:          
                print("Error:", e.error)
                await manager.send_personal_message("Error...S", websocket)
                continue

            # print("\n\n\n history:", chat_history_store)
            # print("\n\nFinal response:\n", final_response.message.content)

            # for chunk in final_response:
            #   await websocket.send_text(f"{chunk['message']['content']}")
            #   print(chunk['message']['content'], end='', flush=True)

            end_time = time.time()
            elapsed_time = end_time - start_time
            await manager.send_personal_message(final_response.message.content + ' **time take:' + str(round(elapsed_time)) +  ' second' , websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
