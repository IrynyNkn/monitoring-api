from celery import signals

from app.entrypoint import app


@app.celery.task(name="continuous_ping")
def continuous_ping(ping_id: str) -> None:
    app.ping_service.ping(ping_id)


@app.celery.task(name="continuous_health_check")
def continuous_health_check(health_check_id: str) -> None:
    app.health_check_service.perform_health_check(health_check_id)


@app.celery.task(name="kube_metrics_collecting")
def kube_metrics_collecting() -> None:
    try:
        metrics = app.kube_metrics_service.retrieve_kube_dynamic_metrics()
        print("Collected kube metrics fired")
    except Exception as exc:
        print("Exception in celery task kube_metrics_collection", exc)


@signals.worker_init.connect
def worker_process_init(*args, **kwargs):
    print("Starting celery task kube_metrics_collection")
    kube_metrics_collecting.delay()
