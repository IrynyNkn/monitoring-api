from fastapi import APIRouter

from .endpoints.icmp_ping import router as ping_router


router = APIRouter()

router.include_router(ping_router)
