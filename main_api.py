from fastapi import FastAPI , UploadFile , File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from dotenv import load_dotenv

load_dotenv()

# Import your Month 1 modules
from llm.joi import get_reply_non_streaming
from txt_to_speech.tts import speak


app = FastAPI()

# CORS — allows browser to call this API
# Without this, browser requests get blocked
class TextInput(BaseModel):
    message: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # any frontend can call this for now
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello/{name}")
def hello(name:str):
    return {"message" : f"Hello, {name}!"}

@app.post("/chat/text")
def chat_text(input: TextInput):
    """handles text input-no need to transcribe"""
    try:
        reply = get_reply_non_streaming(input.message)
        speak(reply)
        return{
            "user_input": input.message,
            "reply" : reply,
            "status": "ok"
        }
    except Exception as e:
        return{
            "error":str(e),
            "status": "error"
        }

@app.post("/chat/voice")
async def chat_voice(audio : UploadFile = File(...)):
    """handles voice input-- need for transcribing"""
    try:
        temp_path = "temp_uload.wav"
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(audio.file, f)

        from voice.input import transcribe
        user_text = transcribe(temp_path)
        if not user_text:
            return {"error": "Could not transcribe audio", "status": "error"}
        reply = get_reply_non_streaming(user_text)
        speak(reply)
        return{
            "user_input": user_text,
            "reply": reply,
            "status": "ok"
        }
    except Exception as e:
        return{
            "error":str(e),
            "status": "error"
        }

@app.get("/health")
def health():
    return {"status": "ok"}