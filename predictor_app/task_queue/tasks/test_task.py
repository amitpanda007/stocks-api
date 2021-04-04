from datetime import time

from predictor_app.task_queue.celery_config import celery


@celery.task()
def add_together(a, b):
    # time.sleep(5)
    return a + b