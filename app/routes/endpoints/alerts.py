from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.routes.serializers import CreateAlert, User
from app.routes.auth.get_user import get_current_user

router = APIRouter(prefix="/alerts")


@router.get("/", status_code=status.HTTP_200_OK)
def get_alerts(current_user: User = Depends(get_current_user)):
    from app.entrypoint import app

    alerts = app.alerts_crud_service.get_alerts(current_user.id)

    return JSONResponse({"alerts": alerts})


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_alert(alert_data: CreateAlert, current_user: User = Depends(get_current_user)):
    from app.entrypoint import app

    created_alert_id = app.alerts_crud_service.create_alert(alert_data, current_user.id)

    return JSONResponse({"alert_id": created_alert_id})


@router.put("/{alert_id}", status_code=status.HTTP_200_OK)
def update_alert(alert_id, alert_data: CreateAlert, current_user: User = Depends(get_current_user)):
    from app.entrypoint import app

    updated_alert_id = app.alerts_crud_service.update_alert(alert_data, alert_id)

    return JSONResponse({"alert_id": updated_alert_id})


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_alert(alert_id, current_user: User = Depends(get_current_user)):
    from app.entrypoint import app

    deleted_alert_id = app.alerts_crud_service.delete_alert(alert_id)

    return JSONResponse({"alert_id": deleted_alert_id})
