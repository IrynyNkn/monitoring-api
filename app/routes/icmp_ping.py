from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from uuid import uuid4
import json
from app.celery_worker import continuous_ping


class UpdatePing(BaseModel):
    interval: int


router = APIRouter()


@router.get("/icmp-ping")
async def icmp_ping(host: str, interval: int, request: Request):
    task_id = str(uuid4())
    task_info = {
        "host": host,
        "interval": interval,
        "status": "active"
    }

    redis = request.app.state.redis_client
    await redis.set(task_id, json.dumps(task_info))

    task = continuous_ping.delay(host, interval, task_id)
    return JSONResponse({"Task Result:": task.id})


@router.post("/icmp-ping/update-ping/{task_id}")
async def update_ping_task(req_body: UpdatePing, task_id: str, request: Request):
    redis = request.app.state.redis_client

    ping_config_json = await redis.get(task_id)
    ping_config = json.loads(ping_config_json)
    ping_config['interval'] = req_body.interval
    await redis.set(task_id, json.dumps(ping_config))

    return JSONResponse({"status": "updated", "task_id": task_id})


@router.delete("/icmp-ping/cancel-ping/{task_id}")
async def cancel_ping_task(task_id: str, request: Request):
    await request.app.state.redis_client.delete(task_id)
    # celery.control.revoke(task_id, terminate=True)
    return JSONResponse({"status": "cancelled", "task_id": task_id})


# @router.get("/icmp-ping/get-example")
# async def get_example(request: Request):
#     redis = request.app.state.redis_client
#     value = await redis.get("my-key")
#     return {"message": "Value set successfully", "value": value}
#
#
# @router.get("/icmp-ping/set-example")
# async def set_example(request: Request):
#     redis = request.app.state.redis_client
#     await redis.set("my-key", "my-value")
#     return {"message": "Value set successfully"}


# @router.get("/icmp-ping/test")
# async def test():
#     return {"message": "Success"}

# @router.get("/icmp-ping/test-celery")
# def test_celery():
#     task = create_task.delay()
#     return JSONResponse({"Task Result:": "nice"})

# @router.get("/icmp-ping")
# async def icmp_ping(host: str, interval: int):
#     task = continuous_ping.delay(host, interval)
#     return JSONResponse({"Task Result:": task.id})
