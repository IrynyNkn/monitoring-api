from fastapi import FastAPI
import redis.asyncio as redis
from .routes import icmp_ping_router


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    app.state.redis_client = redis.Redis(host='redis', port=6379, decode_responses=True, db=1)


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.redis_client.aclose()


app.include_router(icmp_ping_router)


# @app.get("/set-example")
# async def set_example():
#     # print(f"Ping successful: {await app.state.redis_client.ping()}")
#     # return {"message": "Value set successfully"}
#
#     await app.state.redis_client.set("my-key", "my-value")
#     return {"message": "Value set successfully"}

    # print("REDIS", app.state.redis)
    # if app.state.redis is not None:
    #     await app.state.redis.set('my-key', 'my-value')
    #     return {"message": "Value set successfully"}

    # return {"message": "Value set failed"}


# @app.get("/get-example")
# async def get_example():
#     # print(f"Ping successful: {await app.state.redis_client.ping()}")
#     # return {"message": "Value set successfully"}
#
#     value = await app.state.redis_client.get("my-key")
#     return {"message": "Value set successfully", "value": value}

