from fastapi import APIRouter

from app.api_v1.endpoints import auth, users, domains, items, scraping_urls, scraping_tasks, chatbots, chats, faqs

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
# api_router.include_router(domain.router, prefix="/domains", tags=["domains"])

# Chat functionality
# api_router.include_router(chat_ws.router, prefix="/chat", tags=["chat"])

# Domain management
api_router.include_router(domains.router, prefix="/domains", tags=["domains"])

# Web scraping
api_router.include_router(scraping_urls.router, prefix="/scraping/urls", tags=["scraping"])
api_router.include_router(scraping_tasks.router, prefix="/scraping", tags=["scraping"])

# Chatbot management
api_router.include_router(chatbots.router, prefix="/chatbots", tags=["chatbots"])
api_router.include_router(chats.router, prefix="/chats", tags=["chats"])
api_router.include_router(faqs.router, prefix="/faqs", tags=["faqs"])