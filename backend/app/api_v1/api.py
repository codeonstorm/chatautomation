from fastapi import APIRouter

from app.api_v1.routes import plans
from app.api_v1.routes import users
from app.api_v1.routes import auth
from app.api_v1.routes import chatbots
from app.api_v1.routes import domains
from app.api_v1.routes import resumable

api_router = APIRouter()
api_router.include_router(plans.router)
api_router.include_router(users.router)
api_router.include_router(auth.router)
api_router.include_router(chatbots.router)
api_router.include_router(domains.router)
api_router.include_router(resumable.router)