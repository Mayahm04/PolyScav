from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
from datetime import datetime

from database import SessionLocal, Prediction, Base, engine
from model import predict_image, predict_text

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartSort Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/predict/image")
async def predict_image_route(file: UploadFile = File(...)):

    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    category = predict_image(img)

    db = SessionLocal()
    pred = Prediction(
        input="image",
        output=category,
        type="image",
        timestamp=datetime.now()
    )
    db.add(pred)
    db.commit()
    db.close()

    return JSONResponse({"prediction": category})


@app.post("/predict/text")
async def predict_text_route(description: str = Form(...)):

    category = predict_text(description)

    db = SessionLocal()
    pred = Prediction(
        input=description,
        output=category,
        type="text",
        timestamp=datetime.now()
    )
    db.add(pred)
    db.commit()
    db.close()

    return JSONResponse({"prediction": category})


@app.get("/history")
def get_history():

    db = SessionLocal()
    preds = db.query(Prediction).order_by(Prediction.timestamp.desc()).all()
    db.close()

    return [
        {
            "id": p.id,
            "input": p.input,
            "output": p.output,
            "type": p.type,
            "timestamp": p.timestamp
        }
        for p in preds
    ]
