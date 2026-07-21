from fastapi import FastAPI, Request
import asyncio
import time
from groq import Groq

app = FastAPI()

# Make sure your actual Groq API key is inserted here
GROQ_API_KEY = "gsk_..."  # <--- REPLACE WITH YOUR REAL GROQ KEY
client = Groq(api_key=GROQ_API_KEY)

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    data = await request.json()
    user_messages = data.get("messages", [])
    
    # Simple, safe system prompt
    system_prompt = {
        "role": "system",
        "content": "You are a casual student texting a friend. Keep replies short, lower-case, and informal."
    }
    
    # 1. Non-blocking typing delay (1.5 seconds)
    await asyncio.sleep(1.5)
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[system_prompt] + user_messages,
            temperature=0.7,
            max_tokens=150
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = "my net is lagging badly bro, say again?"

    # OpenAI-compatible response structure
    return {
        "id": "chatcmpl-ghostprotocol-001",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "ghost-in-the-chat",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": reply
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 15,
            "completion_tokens": 15,
            "total_tokens": 30
        }
    }