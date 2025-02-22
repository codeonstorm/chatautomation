from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Middleware to handle CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # Allows all origins
  allow_credentials=True,
  allow_methods=["*"],  # Allows all methods
  allow_headers=["*"],  # Allows all headers
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
  response = await call_next(request)
  response.headers["X-Process-Time"] = str(request.state.process_time)
  return response

@app.get("/")
async def read_root():
  return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
  return {"item_id": item_id, "q": q}