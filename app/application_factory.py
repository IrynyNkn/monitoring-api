from app import constants
from app.routes import router
from app.routes.endpoints.external_ping import router as external_ping_router
from app.settings import AppSettings
from app.application_builder import ApplicationBuilder
from app.application import Application


class ApplicationFactory:

    def create_internal_application(self) -> Application:
        return (
            ApplicationBuilder.from_config(AppSettings())
            .with_redis()
            .with_celery()
            .with_fastapi()
                .with_fastapi_routes(
                    [router],
                    prefix=constants.ROUTER_PATH,
                )
            .with_influxdb()
            .with_postgres()
            .build()
        )

    def create_external_application(self) -> Application:
        return (
            ApplicationBuilder.from_config(AppSettings())
            .with_redis()
            .with_celery()
            .with_fastapi()
            .with_fastapi_routes(
                [external_ping_router],
                prefix=constants.ROUTER_PATH,
            )
            .build()
        )
