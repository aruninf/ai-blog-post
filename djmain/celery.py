import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djmain.settings')

app = Celery('djmain')

# Ensure the Celery app only runs after Django setup
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Ensure Django setup happens before the tasks are registered

# Configure periodic tasks in Celery
app.conf.beat_schedule = {
    'post-blog-every-1-minute': {
        'task': 'blogs.tasks.auto_post_blog',
        'schedule': crontab(minute='*'),  # Runs every 1 minute
    },
}


app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
