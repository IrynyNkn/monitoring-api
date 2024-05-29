from celery import signals


@signals.worker_init.connect
def worker_process_init(*args, **kwargs):
    print("External ping init fired")
