from app.entrypoint import app


@app.celery.task(name="continuous_ping")
def continuous_ping(ping_id: str) -> None:
    app.ping_service.ping(ping_id)


# @app.celery.task(name="kube_metrics_collection")
# def kube_metrics_collection() -> None:
#     print("Starting kube_metrics_collection")
#     return
