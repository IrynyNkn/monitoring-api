import json
import redis
from celery import Celery, signals
from icmplib import ping


celery = Celery(__name__)
celery.conf.broker_url = "redis://redis:6379/0"
celery.conf.result_backend = "redis://redis:6379/0"

redis_client = None


@signals.worker_process_init.connect
def setup_redis(**kwargs):
    print('connected celery to redis')
    global redis_client
    redis_client = redis.Redis(host='redis', port=6379, decode_responses=True, db=1)


@celery.task(name="continuous_ping")
def continuous_ping(host, interval, task_id):
    global redis_client
    ping_config_json = redis_client.get(task_id) if redis_client is not None else None

    print('TASK ID', task_id)
    if ping_config_json is not None:
        ping_config = json.loads(ping_config_json)
        if ping_config['status'] == 'active':
            response = ping(host, count=1)
            if response.packets_received > 0:
                print(f'Ping to {host} succeeded.')
            else:
                print(f'Ping to {host} failed.')

            continuous_ping.apply_async(args=[host, ping_config['interval'], task_id], countdown=interval)
        else:
            print(f'Ping to {host} was canceled.')


# @celery.task(name="create_task")
# def create_task():
#     global redis_client
#     print('REDIS CON:', redis_client)
#     time.sleep(1)
#     return 2 + 2


# @celery.task(name="continuous_ping")
# def continuous_ping(host, interval):
#     while True:
#         response = ping(host, count=1)
#         if response.packets_received > 0:
#             print(f'Ping to {host} succeeded.')
#         else:
#             print(f'Ping to {host} failed.')
#
#         time.sleep(interval)


