import time
from celery import Celery
from icmplib import ping


celery = Celery(__name__)
celery.conf.broker_url = "redis://redis:6379/0"
celery.conf.result_backend = "redis://redis:6379/0"


@celery.task(name="create_task")
def create_task(a, b, c):
    time.sleep(a)
    return b + c


@celery.task(name="continuous_ping_pro")
def continuous_ping_pro(host, interval):
    response = ping(host, count=1)
    if response.packets_received > 0:
        print(f'Ping to {host} succeeded.')
    else:
        print(f'Ping to {host} failed.')

    continuous_ping_pro.apply_async(args=[host, interval], countdown=interval)


@celery.task(name="continuous_ping")
def continuous_ping(host, interval):
    while True:
        response = ping(host, count=1)
        if response.packets_received > 0:
            print(f'Ping to {host} succeeded.')
        else:
            print(f'Ping to {host} failed.')

        time.sleep(interval)


