from icmplib import ping

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/external-ping")


@router.get("", status_code=status.HTTP_200_OK)
def get_icmp_pings():
    response = ping("need to think where to get this value from", count=1)

    return JSONResponse({"rtt": response.avg_rtt})
