import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api_v1.api import api_router
from app.chat.router import chat_router
from app.core.database import create_db_and_tables

load_dotenv()
app = FastAPI(
  title=settings.PROJECT_NAME,
  description=settings.PROJECT_DESCRIPTION,
  version=settings.VERSION,
  openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=settings.CORS_ORIGINS,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)



# @app.exception_handler(HTTPException)
# async def custom_http_exception_handler(request: Request, exc: HTTPException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={
#             "status_code": exc.status_code,
#             "detail": [
#                 {
#                     "loc": request.url.path.split("/"),
#                     "msg": exc.detail,
#                     "type": "error"
#                 }
#             ]
#         },
#     )

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     errors = [
#         {
#             "loc": err["loc"],
#             "msg": err["msg"],
#             "type": err["type"]
#         }
#         for err in exc.errors()
#     ]
#     return JSONResponse(
#         status_code=422,
#         content={
#             "status_code": 422,
#             "detail": errors
#         },
#     )

# @app.get("/example")
# async def example_endpoint(value: int):
#     if value < 0:
#         raise HTTPException(status_code=400, detail="Value must be non-negative")
#     return {"value": value}


# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)
# Include chat router directly at /chat
app.include_router(chat_router)

# @app.on_event("startup")
# def on_startup():
#   create_db_and_tables()

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

