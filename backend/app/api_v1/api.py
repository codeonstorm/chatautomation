from fastapi import APIRouter

from app.api_v1.routes import (
    plans,
    auth,
    users,
    services,
    chatbots,
    domains,
    resumable,
    datasets,
)

api_router = APIRouter()
api_router.include_router(plans.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(services.router)
api_router.include_router(chatbots.router)
api_router.include_router(domains.router)
api_router.include_router(resumable.router)
api_router.include_router(datasets.router)
