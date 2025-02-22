from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/rag/query")
async def rag_query(request: QueryRequest):
    try:
        # Run the LangGraph workflow
        result = app.invoke({"question": request.question})
        return {
            "answer": result['answer'],
            "context": result.get('context', '')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
