from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import asyncio
from typing import Optional

app = FastAPI(title="Human Interaction API", version="1.0.0")

# save the question and user's response
current_question: Optional[str] = None
user_response: Optional[str] = None
response_ready = asyncio.Event()

class QuestionRequest(BaseModel):
    question: str

class ResponseRequest(BaseModel):
    response: str

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Send a question to the user and wait for the user's response"""
    global current_question, user_response, response_ready
    
    current_question = request.question
    user_response = None
    response_ready.clear()
    
    print(f"\n🤖 Question: {current_question}")
    print("Please enter your response above...")
    
    # wait for the user's response
    await response_ready.wait()
    
    return {"response": user_response}

@app.post("/respond")
async def provide_response(request: ResponseRequest):
    """User provides response"""
    global user_response, response_ready
    
    user_response = request.response
    response_ready.set()
    
    return {"status": "success", "message": "Response received"}

@app.get("/status")
async def get_status():
    """Get the current status"""
    return {
        "current_question": current_question,
        "has_response": user_response is not None
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000) 
