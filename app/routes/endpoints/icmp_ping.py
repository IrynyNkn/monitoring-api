from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.routes.serializers import UpdatePing, CreatePing

router = APIRouter(prefix="/ping")


# @router.get("/pings", status_code=status.HTTP_200_OK)
# def get_ping_metrics():
#     from app.entrypoint import app
#
#     data = app.ping_service.get_pings()
#
#     return JSONResponse(data)


@router.get("/{ping_id}", status_code=status.HTTP_200_OK)
def get_ping_metrics(ping_id: str):
    from app.entrypoint import app

    data = app.ping_service.get_ping_metrics(ping_id)

    return JSONResponse(data)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_ping(create_ping_data: CreatePing):
    from app.entrypoint import app

    ping_id = app.ping_service.add_new_ping(host=create_ping_data.host, interval=create_ping_data.interval)

    return JSONResponse({"task_id": ping_id})


@router.put("/{ping_id}", status_code=status.HTTP_200_OK)
def update_ping(update_ping_data: UpdatePing):
    pass


@router.delete("/{ping_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_ping(ping_id: str):
    from app.entrypoint import app

    app.ping_repository.delete(ping_id)

    return JSONResponse({"status": "cancelled", "id": ping_id})
