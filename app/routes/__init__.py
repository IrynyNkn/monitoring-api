from fastapi import APIRouter

from .endpoints.icmp_ping import router as ping_router
from .endpoints.kube_metrics import router as kube_metrics_router
from .endpoints.accounts import router as accounts_router
from .endpoints.alerts import router as alerts_router
from .endpoints.http_health_checks import router as health_checks_router


router = APIRouter()

router.include_router(ping_router)
router.include_router(kube_metrics_router)
router.include_router(accounts_router)
router.include_router(alerts_router)
router.include_router(health_checks_router)
