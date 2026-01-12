from fastapi import APIRouter, WebSocket
from vosk import Model, KaldiRecognizer
import json
from app.utilis.token_utilis import verify_token

voice_router = APIRouter(prefix="/voice", tags=["Voice"])

model = Model("app/vosk-model/vosk-model-small-en-us-0.15")

@voice_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token or not verify_token(token):
        await websocket.close(code=403)
        return

    await websocket.accept()
    recognizer = KaldiRecognizer(model, 16000)

    try:
        while True:
            data = await websocket.receive_bytes()  # 🔥 audio from browser
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    await websocket.send_text(json.dumps({
                        "text": text,
                        "final": True
                    }))
            else:
                partial = json.loads(recognizer.PartialResult()).get("partial", "")
                if partial:
                    await websocket.send_text(json.dumps({
                        "text": partial,
                        "final": False
                    }))
    except Exception as e:
        print("WebSocket closed:", e)

