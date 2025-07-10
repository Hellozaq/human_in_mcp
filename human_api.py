from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import asyncio
from typing import Optional, Dict
from collections import deque
import uuid

app = FastAPI(title="Human Interaction API", version="1.0.0")

# use deque to manage multiple requests
request_queue = deque()
pending_requests: Dict[str, asyncio.Event] = {}
request_responses: Dict[str, str] = {}

class QuestionRequest(BaseModel):
    question: str

class ResponseRequest(BaseModel):
    response: str
    request_id: Optional[str] = None

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Send a question to the user and wait for the user's response"""
    global request_queue, pending_requests, request_responses
    
    # generate a unique request id
    request_id = str(uuid.uuid4())
    
    # create an event to wait for the response
    response_event = asyncio.Event()
    pending_requests[request_id] = response_event
    
    # add the request to the queue
    request_queue.append({
        "id": request_id,
        "question": request.question
    })
    
    print(f"\n🤖 Question [{request_id}]: {request.question}")
    print("Please enter your response above...")
    print(f"Use request_id: {request_id} when responding")
    
    # wait for the user's response
    await response_event.wait()
    
    # get the response and clean up
    response = request_responses.pop(request_id, "No response received")
    pending_requests.pop(request_id, None)
    
    return {"response": response, "request_id": request_id}

@app.post("/respond")
async def provide_response(request: ResponseRequest):
    """User provides response"""
    global pending_requests, request_responses
    
    request_id = request.request_id
    
    if not request_id:
        # if no request_id is specified, use the first request in the queue
        if request_queue:
            request_id = request_queue[0]["id"]
            request_queue.popleft()
        else:
            raise HTTPException(status_code=400, detail="No pending requests")
    
    if request_id not in pending_requests:
        raise HTTPException(status_code=400, detail=f"Request {request_id} not found or already responded")
    
    # save the response and set the event
    request_responses[request_id] = request.response
    pending_requests[request_id].set()
    
    return {"status": "success", "message": f"Response received for request {request_id}"}

@app.get("/status")
async def get_status():
    """Get the current status"""
    global request_queue, pending_requests
    
    current_question = None
    if request_queue:
        current_question = request_queue[0]["question"]
    
    return {
        "pending_requests": len(request_queue),
        "current_question": current_question,
        "total_pending": len(pending_requests)
    }

@app.get("/queue")
async def get_queue():
    """Get the current request queue"""
    global request_queue
    
    return {
        "queue": [
            {"id": req["id"], "question": req["question"]} 
            for req in request_queue
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000) 
