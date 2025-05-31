from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
    status,
    Request,
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
from app.models.intents import Intent

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.schemas.chathistory import ChatHistoryRead, KnownUserRead
from app.classes.ner.regex_ner_extractor import RegexNERExtractor
from app.classes.ner.synonym_ner_extractor import SynonymNERExtractor
from app.schemas.context_store import ContextStore
from app.models.entities import Entities
from app.classes.chat_flow import ChatFlow

from app.services.intent_service import (
    get_all_intents
)
from app.services.webhook_service import get_webhook_service

MODEL_DIR = Path("models")
model = SetFitModel.from_pretrained(
    MODEL_DIR / "buybot_setfit_model" / "buybot_setfit_model"
)

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
    request: Request, encodedid: str, session: Session = Depends(get_session)
):
    decoded = base64.b64decode(encodedid).decode("utf-8")
    part = decoded.split("|")
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

    return templates.TemplateResponse(
        "chatbot.html",
        {
            "request": request,
            "chatbot": chatbot,
        },
    )


@chat_router.websocket("/{encodedid}/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    encodedid: str,
    token: UUID,
    session: Session = Depends(get_session),
):
    """
    WebSocket endpoint for chat
    """
    decoded = base64.b64decode(encodedid).decode("utf-8")
    part = decoded.split("|")
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
            user_data=str(
                {
                    "name": "Unknown",
                    "email": "Unknown",
                    "phone": "Unknown",
                }
            ),
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
            await manager.send_personal_message("user: " + history.msg, websocket)
        elif history.type == MessageTypeEnum.assistant:
            await manager.send_personal_message("assistant: " + history.msg, websocket)

    # Initialize chat flow

    # intent
    intentsList = get_all_intents(UUID(chatbot_uuid), session)
    intents = {}

    for intent in intentsList:      
        intents[intent.name] = intent
    del intentsList

    # print("\n\n\n\nintents: ", intents, end="\n\n")

    # entities
    entities = session.exec(
        select(Entities).where(Entities.chatbot_uuid == UUID(chatbot_uuid))
    ).all()
    
    entitiesSynonymList = {}
    entitiesPatternList = {}
    # for entity in entities:
    #     if entity.entity_type == "list":
    #         entity.value = json.loads(entity.value) if entity.value else None
    #         entitiesSynonymList[entity.name] = entity.value
    #     elif entity.entity_type == "pattern":
    #         entity.value = json.loads(entity.value) if entity.value else None
    #         entitiesPatternList[entity.name] = (
    #             entity.value[entity.name][0] if entity.value else None
    #         )

    entitiesList = {
        "synonym": entitiesSynonymList,
        "pattern": entitiesPatternList,
    }
    del entitiesSynonymList
    del entitiesPatternList

    # print("\n\n\n\nentitiesList: ", entitiesList, end="\n\n")

    webhook_config = get_webhook_service(UUID(chatbot_uuid), session)

    chatFlow: ChatFlow = ChatFlow(model, intents, entitiesList, webhook_config)
    try:
        while True:
            data = await websocket.receive_json()
            user_message_str = data.get("message", "")
            if not user_message_str:
                continue

            # user query entry
            chathistory = ChatHistory(
                chatuser=user.uuid,
                type=MessageTypeEnum.user,
                feedback=FeedbackEnum.neutral,
                msg=user_message_str,
            )
            session.add(chathistory)
            session.commit()

            reply = chatFlow.chat(user_message_str)

            # bot reply entry
            chathistory = ChatHistory(
                chatuser=user.uuid,
                type=MessageTypeEnum.assistant,
                feedback=FeedbackEnum.neutral,
                msg=reply,
            )
            session.add(chathistory)
            session.commit()

            await manager.send_personal_message(reply, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# chathistory
#  auth pending ..
@chat_router.get("/{chatbot_uuid}/users", response_model=List[KnownUserRead])
async def read_chat_history(
    chatbot_uuid: UUID, session: Session = Depends(get_session)
):
    user = session.exec(
        select(KnownUser).where(KnownUser.chatbot_uuid == chatbot_uuid)
    ).all()
    if not user:
        raise HTTPException(status_code=404, detail="not find user")

    knownUserArr = []
    for user in user:
        latest_chat = session.exec(
            select(ChatHistory)
            .where(ChatHistory.chatuser == user.uuid)
            .order_by(ChatHistory.timestamp.desc())
            .limit(1)
        ).first()

        json_str = user.user_data.replace(
            "'", '"'
        )  # replace single quotes with double quotes
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
                latest_msg=(
                    ChatHistoryRead(
                        id=latest_chat.id,
                        chatuser=latest_chat.chatuser,
                        type=latest_chat.type.value,
                        msg=latest_chat.msg,
                        feedback=(
                            latest_chat.feedback.value if latest_chat.feedback else None
                        ),
                        timestamp=latest_chat.timestamp,
                    )
                    if latest_chat
                    else None
                ),
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


@chat_router.get(
    "/{chatbot_uuid}/history/{chatuser_uuid}", response_model=List[ChatHistoryRead]
)
async def chat_users(chatuser_uuid: UUID, session: Session = Depends(get_session)):
    chat_history = session.exec(
        select(ChatHistory).where(ChatHistory.chatuser == chatuser_uuid)
    ).all()

    if not chat_history:
        return []
    return chat_history
