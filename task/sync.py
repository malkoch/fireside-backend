from task.celery import celery


@celery.task
def sync_data():
    print('running data sync method')
