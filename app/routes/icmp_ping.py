from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.celery_worker import continuous_ping, continuous_ping_pro, celery

router = APIRouter()


@router.get("/icmp-ping/test")
async def test():
    return {"message": "Success"}


@router.get("/icmp-ping/get-example")
async def get_example(request: Request):
    redis = request.app.state.redis_client
    value = await redis.get("my-key")
    return {"message": "Value set successfully", "value": value}


@router.get("/icmp-ping/set-example")
async def set_example(request: Request):
    redis = request.app.state.redis_client
    await redis.set("my-key", "my-value")
    return {"message": "Value set successfully"}


# @app.post("/test-celery")
# def test_celery(amount: str, a: str, b: str):
#     task = create_task.delay(int(amount), int(a), int(b))
#     return JSONResponse({"Task Result:": task.get()})

@router.get("/icmp-ping")
async def icmp_ping(host: str, interval: int):
    task = continuous_ping.delay(host, interval)
    return JSONResponse({"Task Result:": task.id})


@router.get("/icmp-ping-pro")
async def icmp_ping_pro(host: str, interval: int):
    # task_id = str(uuid4())
    # task_info = {"host": host, "interval": interval, "status": "scheduled"}
    # await r.set(task_id, json.dumps(task_info))  # Store task info in Redis
    task = continuous_ping_pro.delay(host, interval)
    return JSONResponse({"Task Result:": task.id})


@router.delete("/cancel-ping/{task_id}")
async def cancel_ping_task(task_id: str):
    celery.control.revoke(task_id, terminate=True)
    return JSONResponse({"status": "cancelled", "task_id": task_id})
