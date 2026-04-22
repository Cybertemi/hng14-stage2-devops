from fastapi import FastAPI, HTTPException
import redis
import uuid
import os
import time

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


def get_redis():
    for _ in range(5):
        try:
            return redis.Redis(
                host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        except Exception:
            time.sleep(1)
    raise Exception("Redis not available")


r = get_redis()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jobs")
def create_job():
    try:
        job_id = str(uuid.uuid4())
        r.lpush("job", job_id)
        r.hset(f"job:{job_id}", "status", "queued")
        return {"job_id": job_id}
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": status}
