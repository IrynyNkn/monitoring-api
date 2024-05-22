from fastapi import APIRouter, status, Depends, HTTPException, Query
from fastapi.responses import JSONResponse, Response

from app.routes.serializers import UpdatePing, CreatePing, PausePing
from app.routes.auth.get_user import get_current_user
from app.routes.serializers import User

router = APIRouter(prefix="/ping")


@router.get("/pings", status_code=status.HTTP_200_OK)
def get_icmp_pings(current_user: User = Depends(get_current_user)):
    from app.entrypoint import app

    pings = app.ping_service.get_pings(current_user.id)

    return JSONResponse({"icmp_pings": pings})


@router.get("/{ping_id}", status_code=status.HTTP_200_OK)
def get_ping_metrics(ping_id: str, time_range: str = Query(None)):
    from app.entrypoint import app
    data = app.ping_service.get_ping_metrics(ping_id, time_range)

    return JSONResponse(data)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_ping(create_ping_data: CreatePing, current_user: User = Depends(get_current_user)):
    from app.entrypoint import app

    ping_id = app.ping_service.add_new_ping(
        host=create_ping_data.host,
        interval=create_ping_data.interval,
        owner_id=current_user.id
    )

    return JSONResponse({"task_id": ping_id})


@router.put("/{ping_id}", status_code=status.HTTP_200_OK)
def update_ping(ping_id, upd_ping_data: UpdatePing):
    from app.entrypoint import app

    ping_id = app.ping_service.update_ping(ping_id, upd_ping_data.interval)
    if ping_id:
        return JSONResponse({"status": "updated", "id": ping_id})

    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{ping_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_ping(ping_id: str):
    from app.entrypoint import app

    deleted_ping_id = app.ping_service.delete_ping(ping_id)

    if deleted_ping_id:
        return JSONResponse({"status": "cancelled", "id": ping_id})

    raise HTTPException(status.HTTP_400_BAD_REQUEST)


@router.put("/pause/{ping_id}", status_code=status.HTTP_204_NO_CONTENT)
def pause_ping(ping_id):
    from app.entrypoint import app

    ping_id = app.ping_service.pause_ping(ping_id)
    if ping_id:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/resume/{ping_id}", status_code=status.HTTP_204_NO_CONTENT)
def pause_ping(ping_id):
    from app.entrypoint import app

    ping_id = app.ping_service.resume_ping(ping_id)
    if ping_id:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)