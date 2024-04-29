from fastapi import APIRouter

from .endpoints.icmp_ping import router as ping_router
from .endpoints.kube_metrics import router as kube_metrics_router
from .endpoints.accounts import router as accounts_router


router = APIRouter()

router.include_router(ping_router)
router.include_router(kube_metrics_router)
router.include_router(accounts_router)
