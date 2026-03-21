import redis
from rq import Worker, Queue
redis_conn = redis.Redis(host="localhost", port=6379)
worker = Worker(["fact-check"], connection=redis_conn)
if __name__ == "__main__":
    worker.work()