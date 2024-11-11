from fastapi import FastAPI, HTTPException
from rq import Queue
from redis import Redis
import os
import time
from rq.job import get_current_job


app = FastAPI()
redis_conn = Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379)
queue = Queue(connection=redis_conn)

@app.post("/new1")
def create_task_1(task_data: dict):
    job = queue.enqueue(some_task_1, task_data)
    return {"job_id": job.id}

@app.post("/new2")
def create_task_2(task_data: dict):
    job = queue.enqueue(some_task_2, task_data)
    return {"job_id": job.id}

@app.get("/status/{job_id}")
def get_job_status(job_id: str):
    job = queue.fetch_job(job_id)
    
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    status = {
        "id": job.id,
        "status": job.get_status(),
        "result": job.result if job.is_finished else None,
        "enqueued_at": job.enqueued_at.isoformat() if job.enqueued_at else None,
        "started_at": job.started_at.isoformat() if job.started_at else None,
        "ended_at": job.ended_at.isoformat() if job.ended_at else None,
        "exc_info": job.exc_info if job.is_failed else None
    }
    
    return status

async def some_task_1(data):
    job = get_current_job()
    iters = data.get('iters', 10)
    
    for i in range(1, iters+1):
        print(f"{job.id}: {i}")
        time.sleep(1)
    
    return {"iters": i, 'job_id': job.id, "reverse": False}

def some_task_2(data):
    job = get_current_job()
    iters = data.get('iters', 10)
    
    for i in range(iters, 0, -1):
        print(f"{job.id}: {i}")
        time.sleep(1)
    
    return {"iters": i, 'job_id': job.id, "reverse": True}
