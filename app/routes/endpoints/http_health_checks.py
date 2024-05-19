from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.routes.serializers import CreateHealthCheck, UpdatePing
from app.routes.auth.get_user import get_current_user
from app.routes.serializers import User

router = APIRouter(prefix="/health-checks")


@router.get("/{health_check_id}", status_code=status.HTTP_200_OK)
def get_health_check_metrics(health_check_id: str, current_user: User = Depends(get_current_user)):
    from app.entrypoint import app

    data = app.health_check_service.get_health_check_metrics(health_check_id)

    return JSONResponse(data)


@router.get("/", status_code=status.HTTP_200_OK)
def get_health_checks(current_user: User = Depends(get_current_user)):
    from app.entrypoint import app

    health_checks = app.health_check_service.get_health_checks_list(current_user.id)

    return JSONResponse({"health_checks": health_checks})


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_health_check(health_check_data: CreateHealthCheck, current_user: User = Depends(get_current_user)):
    from app.entrypoint import app

    health_check_id = app.health_check_service.initialize_health_check(current_user.id, health_check_data)

    return JSONResponse({"task_id": health_check_id})


@router.put("/{health_check_id}", status_code=status.HTTP_200_OK)
def update_ping(health_check_id: str, upd_data: UpdatePing, _: User = Depends(get_current_user)):
    from app.entrypoint import app

    health_check_id = app.health_check_service.update_health_check(health_check_id, upd_data.interval)
    if health_check_id:
        return JSONResponse({"status": "updated", "id": health_check_id})

    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{health_check_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_ping(health_check_id: str, _: User = Depends(get_current_user)):
    from app.entrypoint import app

    deleted_health_check_id = app.health_check_service.delete_health_check(health_check_id)
    if deleted_health_check_id:
        return JSONResponse({"status": "cancelled", "id": health_check_id})

    raise HTTPException(status.HTTP_400_BAD_REQUEST)
