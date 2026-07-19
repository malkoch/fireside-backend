from celery import Celery


celery = Celery('task', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
celery.conf.timezone = 'UTC'
celery.conf.beat_schedule = {
    'sync-every-15-seconds': {
        'task': 'task.sync.sync_data',
        'schedule': 15
    },
    'user-every-15-seconds': {
        'task': 'task.user.sync_data',
        'schedule': 15
    }
}
celery.conf.imports = ('task.sync', 'task.user',)
