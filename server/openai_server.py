"""
python main_promptfoo.py

curl http://localhost:8010/chat/completions -X POST -H "Content-Type: application/json" -d '{
  "model": "Qwen/Qwen2.5-1.5B-Instruct",
  "messages": [{"role": "user", "content": "123*456="}],
  "stream": true
}'

curl -X POST http://localhost:8010/restart
"""
# main.py
import os
import uvicorn
import subprocess
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from transformers import AutoTokenizer
from pathlib import Path
import asyncio
N_PREDICT = 20
REPEAT_PENALTY = 1.05
HOME = Path.home()
UMBRELLA="/home/skymizer/20250916/ecosystem-umbrella"
SCRIPT_PATH="/home/skymizer/quality_check/qwen_test/oneshot_fp16.sh"
SYSTEM_PROMPT = "You are a helpful assistant. When answering, unless requested otherwise, give the answer directly without explaining your thought process."
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str
    def dump(self):
        return {"role": self.role, "content": self.content}

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    n: Optional[int] = None
    stream: Optional[bool] = None
    stop: Optional[List[str]] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None

class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: str

class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Optional[Dict[str, Any]] = None


@app.post("/chat/completions")
@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    import time
    import asyncio
    import json
    import uuid
    import pexpect

    # last_user_message = next(
    #     (m.content for m in reversed(request.messages) if m.role == "user"), "Hello!"
    # )
    tokenizer = AutoTokenizer.from_pretrained(request.model)
    prompts = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + [m.dump() for m in request.messages]
    inputs = tokenizer.apply_chat_template(
        prompts,
        add_generation_prompt=True,
        tokenize=False
    )
    print(inputs)
    result = subprocess.run(
        ["/bin/bash", str(SCRIPT_PATH), inputs],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    print(result.stdout)
    # Parse the result and structure it like OpenAI API
    response_data = {
        "id": "chatcmpl-123",  # Example ID, you can generate a unique one
        "object": "chat.completion",
        "created": int(time.time()),  # Current timestamp
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": result.stdout.strip()
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 0,  # Replace with actual token count if available
            "completion_tokens": len(result.stdout.split()),  # Approximate token count
            "total_tokens": len(result.stdout.split())  # Approximate token count
        }
    }

    return JSONResponse(content=response_data)

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8010)
