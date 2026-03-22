import uuid
from threading import Thread
from backend.pipeline import verify_article
jobs = {}
def process_job(job_id, text, url):
    try:
        result = verify_article(text, url)
        jobs[job_id] = {
            "status": "finished",
            "result": result
        }
    except Exception as e:
        jobs[job_id] = {
            "status": "error",
            "error": str(e)
        }
def enqueue_article(text, url):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing"}
    thread = Thread(target=process_job, args=(job_id, text, url))
    thread.start()
    return job_id
def get_job_result(job_id):
    return jobs.get(job_id, {"status": "processing"})