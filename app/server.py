from fastapi import FastAPI, UploadFile, File, Form, WebSocket
from pydantic import BaseModel
from PIL import Image
import io
from ultralytics import YOLO
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import base64
import os
from translate_utils import translate_text



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "runs", "detect", "train", "weights", "best.pt")
model = YOLO(MODEL_PATH)
print("Model loaded successfully")


class DetectionResponse(BaseModel):
    label: str
    confidence: float
    box: list
    translation: Optional[str] = None
    
@app.get("/")
async def root():
    return {"message": "Welcome to the Sign Language Detection API!"}

@app.post("/predict", response_model=list[DetectionResponse])
async def predict(file: UploadFile = File(...), language: str = 'English'):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        results = model(image)
        
        detections = []
        for pred in results[0].boxes:
            x1, y1, x2, y2 = pred.xyxy[0]
            conf = pred.conf[0]
            cls = pred.cls[0]
            label = model.names[int(cls)]
            translated_text = translate_text(label, language)
            detection = {
                "label": f"{label}",  
                "confidence": float(conf),
                "box": [float(x1), float(y1), float(x2), float(y2)],
                "translation": translated_text
            }
            detections.append(detection)
        
        return {detections, language}

    except Exception as e:
        return {"error": str(e)}
    


@app.websocket("/ws/predict")
async def websocket_predict(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            try:
                data = await websocket.receive_text()
                image_data = base64.b64decode(data)
                print("Received and decoded image")
                
                try:
                    image = Image.open(io.BytesIO(image_data)).convert("RGB")
                    print("Image converted to PIL.Image")
                except Exception as e:
                    print(f"Error converting image: {e}")
                    await websocket.send_json({"error": "Invalid image data"})
                    continue
                
                results = model(image, conf=0.15)
                detections = []
                
                if len(results[0].boxes) == 0:
                    print("No detections in this frame.")
                else:
                    for pred in results[0].boxes:
                        conf = pred.conf[0]
                        cls = pred.cls[0]
                        label = model.names[int(cls)]
                        detection = {
                            "label": f"{label}",
                            "confidence": float(conf),
                        }
                        detections.append(detection)
                
                print("Sending detections:", detections)
                await websocket.send_json(detections)
            except Exception as e:
                print(f"Error processing frame: {e}")
                await websocket.send_json({"error": str(e)})
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()
