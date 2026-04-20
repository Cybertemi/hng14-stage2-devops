import redis
import time
import os
import signal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

running = True

def shutdown(signum, frame):
    global running
    running = False

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

def connect_redis():
    for _ in range(5):
        try:
            return redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                decode_responses=True
            )
        except Exception:
            time.sleep(1)
    raise Exception("Redis connection failed")

r = connect_redis()

def process_job(job_id):
    try:
        logger.info(f"Processing job {job_id}")
        time.sleep(2)

        r.hset(f"job:{job_id}", "status", "completed")
        logger.info(f"Done: {job_id}")

    except Exception as e:
        logger.error(f"Error processing job {job_id}: {e}")
        r.hset(f"job:{job_id}", "status", "failed")

while running:
    job = r.brpop("job", timeout=5)

    if job:
        _, job_id = job
        process_job(job_id)
    else:
        time.sleep(1)
