from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rag_engine import chatbot

app = FastAPI()

# Allow CORS so the Chrome Extension can talk to localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the extension ID
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    video_id: str

class ChatRequest(BaseModel):
    question: str

@app.post("/process")
async def process_video(request: VideoRequest):
    try:
        status = chatbot.process_video(request.video_id)
        return {"status": "success", "message": status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = chatbot.answer_question(request.question)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)