from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
from backend.pipeline import verify_article
from backend.ocr import extract_text_from_image
from fastapi.middleware.cors import CORSMiddleware
from backend.image_verify import verify_image_with_clip
import os
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class NewsRequest(BaseModel):
    text: str
    url: str = None
@app.post("/verify")
def verify(news: NewsRequest):
    return verify_article(news.text, news.url)
@app.post("/verify-image")
def verify_image(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    text = extract_text_from_image(file_path)
    result = verify_article(text)
    clip_result = verify_image_with_clip(file_path, text)
    os.remove(file_path)  
    return {
        "extracted_text": text,
        "analysis": result,
        "image_verification": clip_result
    }