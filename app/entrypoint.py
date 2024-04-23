from app import constants
from app.routes import router
from app.settings import AppSettings
from app.application_builder import ApplicationBuilder


app = (
    ApplicationBuilder.from_config(AppSettings())
    .with_redis()
    .with_celery()
    .with_fastapi()
        .with_fastapi_routes(
            [router],
            prefix=constants.ROUTER_PATH,
        )
    .with_influxdb()
    .build()
)

from app.metrics.celery_tasks import *

fastapi_app = app.fastapi
celery_app = app.celery
