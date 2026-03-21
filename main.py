from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os
from backend.pipeline import verify_article
from backend.ocr import extract_text_from_image
from backend.image_verify import verify_image_with_clip
from backend.task import enqueue_article, get_job_result
app = FastAPI()
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
    image_result = verify_image_with_clip(file_path, text)
    os.remove(file_path)
    return {
        "analysis": result,
        "image_verification": image_result
    }
@app.post("/verify-async")
def verify_async(news: NewsRequest):
    job_id = enqueue_article(news.text, news.url)
    return {"job_id": job_id}
@app.get("/result/{job_id}")
def get_result(job_id: str):
    return get_job_result(job_id)