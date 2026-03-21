import redis
from rq import Queue
from backend.pipeline import verify_article
redis_conn = redis.Redis(host="localhost", port=6379)
q = Queue("fact-check", connection=redis_conn)
def process_article(text, url=None):
    return verify_article(text, url)
def enqueue_article(text, url=None):
    job = q.enqueue(process_article, text, url)
    return job.id
def get_job_result(job_id):
    from rq.job import Job
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        return {
            "status": job.get_status(),
            "result": job.result
        }
    except:
        return {"status": "error"}