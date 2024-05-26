from app.application_factory import ApplicationFactory
from app.settings import AppSettings


application_is_external = AppSettings().is_external
factory = ApplicationFactory()

app = factory.create_external_application() if application_is_external else factory.create_internal_application()

if application_is_external:
    fastapi_app = app.fastapi
else:
    from app.metrics.celery_tasks import *

    fastapi_app = app.fastapi
    celery_app = app.celery
