from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/external-ping")


@router.get("", status_code=status.HTTP_200_OK)
def get_icmp_pings():
    from app.entrypoint import app

    data = app.external_ping_service.ping()

    if data.get("error"):
        return JSONResponse({"error": "Host not specified"}, status_code=status.HTTP_400_BAD_REQUEST)

    return JSONResponse(data)
