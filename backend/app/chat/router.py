from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
    status,
    Request
)

import base64
from sqlmodel import select, func
from sqlalchemy.orm import aliased

from fastapi import HTTPException
from typing import List

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
from app.models.chathistory import ChatHistory, KnownUser, MessageTypeEnum, FeedbackEnum
from app.schemas.token import TokenPayload
from uuid import uuid4, UUID

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

from app.schemas.chathistory import ChatHistoryRead, KnownUserRead
from app.classes.ner.regex_ner_extractor import RegexNERExtractor
from app.classes.ner.synonym_ner_extractor import SynonymNERExtractor
from app.schemas.context_store import ContextStore

MODEL_DIR = Path("models")
model = SetFitModel.from_pretrained(MODEL_DIR / "buybot_setfit_model" / "buybot_setfit_model")

chat_router = APIRouter(prefix="/chat", tags=["chat"])
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
        # recognize the user here...
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json({"message": message})


manager = ConnectionManager()


@chat_router.get("/{encodedid}", response_class=HTMLResponse)
async def get_chat(
    request: Request,
    encodedid: str,
    session: Session = Depends(get_session)
):
    decoded = base64.b64decode(encodedid).decode('utf-8')
    part = decoded.split('|')
    chatbot_uuid = part[0]
    domain_uuid = part[1]
    
    if not chatbot_uuid or not domain_uuid:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    try:
        chatbot = session.exec(
            select(Chatbot).where(Chatbot.uuid == UUID(chatbot_uuid))
        ).first()
    except Exception as e:
        # print("Error fetching chatbot:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    if not chatbot:
     return HTMLResponse(status_code=404, content="Chatbot not found")

    return templates.TemplateResponse("chatbot.html", {
        "request": request,
        "chatbot": chatbot,
    })


@chat_router.websocket("/{encodedid}/ws")
async def websocket_endpoint(
    websocket: WebSocket, 
    encodedid: str,
    token: UUID,
    session: Session = Depends(get_session)
):
    """
    WebSocket endpoint for chat
    """
    decoded = base64.b64decode(encodedid).decode('utf-8')
    part = decoded.split('|')
    chatbot_uuid = part[0]
    domain_uuid = part[1]
    
    if not chatbot_uuid or not domain_uuid:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    user = session.exec(
        select(KnownUser)
        .where(KnownUser.session_uuid == token)
        .where(KnownUser.chatbot_uuid == UUID(chatbot_uuid))
    ).first()

    if not user:
        user = KnownUser(
            session_uuid=token,
            chatbot_uuid=UUID(chatbot_uuid),
            domain_uuid=UUID(domain_uuid),
            user_data=str({
                "name": "Unknown",
                "email": "Unknown",
                "phone": "Unknown",
            })
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    chathistory = session.exec(
        select(ChatHistory).where(ChatHistory.chatuser == user.uuid)
    ).all()

    await manager.connect(websocket)
    # get chat history form db
    for history in chathistory:
        if history.type == MessageTypeEnum.user:
            await manager.send_personal_message('user: ' + history.msg, websocket)
        elif history.type == MessageTypeEnum.assistant:
            await manager.send_personal_message('assistant: ' + history.msg, websocket)
   
    chat_history_store = []
    context_store: ContextStore = {}
    try:
        while True:
            data = await websocket.receive_json()
            start_time = time.time()
            user_message_str = data.get("message", "")
            standalone_question = ""

            if not user_message_str:
                continue

            # user msg entry
            chathistory = ChatHistory(
                chatuser=user.uuid,
                type=MessageTypeEnum.user,
                feedback=FeedbackEnum.neutral,
                msg=user_message_str,
            )
            session.add(chathistory)
            session.commit()

            if len(user_message_str) <= 2:
                await manager.send_personal_message("Hello! How can I help you today?", websocket)
                # assistant msg entry
                chathistory = ChatHistory(
                    chatuser=user.uuid,
                    type=MessageTypeEnum.assistant,
                    feedback=FeedbackEnum.neutral,
                    msg="Hello! How can I help you today?",
                )
                session.add(chathistory)
                session.commit()
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

                if predicted_intent == 'other':
                    if context_store:
                        predicted_intent = context_store.intent

                if predicted_intent == 'greeting':
                    await manager.send_personal_message("Hello! How can I help you today?", websocket)
                    # assistant msg entry
                    chathistory = ChatHistory(
                        chatuser=user.uuid,
                        type=MessageTypeEnum.assistant,
                        feedback=FeedbackEnum.neutral,
                        msg="Hello! How can I help you today?",
                    )
                    session.add(chathistory)
                    session.commit()
                    continue
                elif predicted_intent == 'goodbye':
                    await manager.send_personal_message("Take care, until next time!", websocket)
                    # assistant msg entry
                    chathistory = ChatHistory(
                        chatuser=user.uuid,
                        type=MessageTypeEnum.assistant,
                        feedback=FeedbackEnum.neutral,
                        msg="Take care, until next time!",
                    )
                    session.add(chathistory)
                    session.commit()
                    continue
                elif predicted_intent == 'restricted_content':
                    await manager.send_personal_message("I'm here to help with respectful, safe, and appropriate topics. Let's keep things positive and productive!", websocket)
                    # assistant msg entry
                    chathistory = ChatHistory(
                        chatuser=user.uuid,
                        type=MessageTypeEnum.assistant,
                        feedback=FeedbackEnum.neutral,
                        msg="I'm here to help with respectful, safe, and appropriate topics. Let's keep things positive and productive!",
                    )
                    session.add(chathistory)
                    session.commit()
                    continue
                elif predicted_intent == 'schedule_meet':
                    # set store
                    #  set intent, context, entity w/ value
                    # check actions

                    # check entities
                    action_arguments = {
                        'email': {
                            'required': True,
                            'msg': 'Please provide email'
                        },
                        'mobile': {
                            'required': True,
                            'msg': 'Mobile number required to schedule meet'
                        }
                    }
                    entities = RegexNERExtractor.extract_entities(user_message_str)
                    print("\n\n\n\nRegexNERExtractor entities: ", entities, end="\n\n")

                    context_store = ContextStore(
                        intent='schedule_meet',
                        context='appointment',
                        entities=entities
                    )

                    print('context', context_store)

                    for arg, arg_props in action_arguments.items():
                        if arg_props.get('required', False):
                            if not entities.get(arg):
                                print(arg_props.get('msg', 'how can i help you'))


                    # check if webhook enabled

                    # default response


                    await manager.send_personal_message("Sorry, I don't have enough information to schedule meeting", websocket)
                    # assistant msg entry
                    chathistory = ChatHistory(
                        chatuser=user.uuid,
                        type=MessageTypeEnum.assistant,
                        feedback=FeedbackEnum.neutral,
                        msg="Sorry, I don't have enough information to schedule meeting",
                    )
                    session.add(chathistory)
                    session.commit()
                    continue
                
                # Standalone Question Preparation
                stand = [Template.condense_question_system_template()]
                for history in chat_history_store:
                    stand.append(history)
                stand.append({"role": "user", "content": user_message_str})
                # print('\n\n stand: ', stand)

                t2 = time.time()
                standalone_response: ChatResponse = chat(
                    "gemma3:1b",
                    # "llama3.2:1b-instruct-q3_K_L",
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

                chathistory = ChatHistory(
                    chatuser=user.uuid,
                    type=MessageTypeEnum.assistant,
                    feedback=FeedbackEnum.neutral,
                    msg=final_response.message.content,
                )
                session.add(chathistory)
                session.commit()
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


# chathistory
#  auth pending ..
@chat_router.get("/{chatbot_uuid}/users", response_model=List[KnownUserRead])
async def read_chat_history(
    chatbot_uuid: UUID,
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(KnownUser).where(KnownUser.chatbot_uuid == chatbot_uuid)
    ).all()
    if not user:
        raise HTTPException(status_code=404, detail="not find user")
    
    knownUserArr = []
    for user in user:
        latest_chat = session.exec(
            select(ChatHistory).where(ChatHistory.chatuser == user.uuid)
            .order_by(ChatHistory.timestamp.desc())
            .limit(1)
        ).first()

        json_str = user.user_data.replace("'", '"')  # replace single quotes with double quotes
        user_data = json.loads(json_str)

        print("\n\n\n\nuser_data ankit: ", user_data, end="\n\n")
        knownUserArr.append(
            KnownUserRead(
                uuid=user.uuid,
                session_uuid=user.session_uuid,
                domain_uuid=user.domain_uuid,
                chatbot_uuid=user.chatbot_uuid,
                user_data=user_data,
                timestamp=user.timestamp,
                latest_msg=ChatHistoryRead(
                    id=latest_chat.id,
                    chatuser=latest_chat.chatuser,
                    type=latest_chat.type.value,
                    msg=latest_chat.msg,
                    feedback=latest_chat.feedback.value if latest_chat.feedback else None,
                    timestamp=latest_chat.timestamp,
                ) if latest_chat else None
            )
        )
    return knownUserArr 


# @chat_router.get("/users", response_model=List[KnownUserRead])
# async def read_chat_history(
#     chatbot_uuid: UUID,
#     session: Session = Depends(get_session)
# ):
#     # Subquery: latest timestamp per session_uuid
#     latest_subq = (
#         select(
#             ChatHistory.session_uuid,
#             func.max(ChatHistory.timestamp).label("latest_ts")
#         ).group_by(ChatHistory.session_uuid)
#         .subquery()
#     )

#     # Alias for joining
#     latest_msg = aliased(ChatHistory)

#     # Main query with JOIN
#     stmt = (
#         select(KnownUser, latest_msg)
#         .join(latest_msg, KnownUser.session_uuid == latest_msg.session_uuid)
#         .join(latest_subq, (latest_msg.session_uuid == latest_subq.c.session_uuid) &
#                            (latest_msg.timestamp == latest_subq.c.latest_ts))
#         .where(KnownUser.chatbot_uuid == chatbot_uuid)
#     )

#     results = session.exec(stmt).all()

#     if not results:
#         raise HTTPException(status_code=404, detail="No users found")

#     # Build response manually
#     return [
#         KnownUserRead(
#             session_uuid=user.session_uuid,
#             domain_uuid=user.domain_uuid,
#             chatbot_uuid=user.chatbot_uuid,
#             user_data=user.user_data,
#             timestamp=user.timestamp,
#             latest_msg=ChatHistoryRead(
#                 session_uuid=msg.session_uuid,
#                 type=msg.type.value,
#                 msg=msg.msg,
#                 feedback=msg.feedback.value if msg.feedback else None,
#                 timestamp=msg.timestamp
#             )
#         )
#         for user, msg in results
#     ]




@chat_router.get("/{chatbot_uuid}/history/{chatuser_uuid}", response_model=List[ChatHistoryRead])
async def chat_users(
    chatuser_uuid: UUID,
    session: Session = Depends(get_session)
):
    chat_history = session.exec(
        select(ChatHistory).where(ChatHistory.chatuser == chatuser_uuid)
    ).all()

    if not chat_history:
        return []
    return chat_history 
