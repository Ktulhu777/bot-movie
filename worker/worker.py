from celery import Celery


from config.config import REDIS_HOST, REDIS_PORT

celery = Celery('worker',
                broker=f'redis://{REDIS_HOST}:{REDIS_PORT}',
                backend=f'redis://{REDIS_HOST}:{REDIS_PORT}',
                broker_connection_retry_on_startup=True)
