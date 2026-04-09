from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import shutil
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

from llm.joi import get_reply_non_streaming, refresh_system_prompt
from txt_to_speech.tts import generate_audio
from voice.input import transcribe
from web_search.tools import load_document


app = FastAPI()



# Serve audio files as static files
#creates the folder if it doesn't exist. exist_ok=True means don't throw an error if it already exists. Always use this when your code depends on a folder existing.
os.makedirs("audio_responses", exist_ok=True)
#StaticFiles — mounts a folder as a static file server. Anything in audio_responses/ is now accessible at /audio/filename.wav. The browser can fetch it directly with a URL.
app.mount("/audio", StaticFiles(directory="audio_responses"), name="audio")

class TextInput(BaseModel):
    message: str

class LoadDocInput(BaseModel):
    filepath: str
    label: str


# CORS — allows browser to call this API
# Without this, browser requests get blocked
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # any frontend can call this for now
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message" : "Joi api is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat/text")
def chat_text(input: TextInput):
    """handles text input-no need to transcribe"""
    try:
        reply = get_reply_non_streaming(input.message)
        filename = f"audio_responses/{uuid.uuid4()}.wav"
 #uuid.uuid4() — generates a unique random ID like a3f8c2d1-.... You use it for filenames so two simultaneous users don't overwrite each other's audio files. Essential for any multi-user system
        audio_path = generate_audio(reply,filename)
        return{
            "user_input": input.message,
            "reply" : reply,
            "audio_url": f"/audio/{os.path.basename(filename)}" if audio_path else None,
            "status": "ok"
        }
    except Exception as e:
        return{
            "error":str(e),
            "status": "error"
        }
#use async def when your function waits on I/O — file uploads, database calls, network requests. Use regular def when it's pure computation with no waiting.
@app.post("/chat/voice")
async def chat_voice(audio : UploadFile = File(...)):
    """handles voice input-- need for transcribing"""
    try:
        upload_path = f"audio_responses/uplaod_{uuid.uuid4()}.wav"
        with open(upload_path, "wb") as f:
            shutil.copyfileobj(audio.file, f)

        user_text = transcribe(upload_path)
        if not user_text:
            return{"error" : "could not transcribe the file", "status":"error"}
        
        reply = get_reply_non_streaming(user_text)

        response_filename = f"audio_responses/{uuid.uuid4()}.wav"
        audio_path = generate_audio(reply, response_filename)

        os.remove(upload_path)

        return{
            "user_input": user_text,
            "reply": reply,
            "audio_url": f"/audio/{os.path.basename(response_filename)}" if audio_path else None,
            "status": "ok"
        }
    except Exception as e:
        return{
            "error":str(e),
            "status": "error"
        }
@app.post("/load-document")
async def ld_doc(input : LoadDocInput):
    """load the pdf for rag"""
    try:
        result = load_document(input.filepath,input.label)
        refresh_system_prompt()
        return {"message": result, "status": "ok"}
    except Exception as e:
        return {"error": str(e), "status": "error"}
