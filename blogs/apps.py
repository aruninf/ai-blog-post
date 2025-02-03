from django.apps import AppConfig
from celery import Celery
from celery.schedules import crontab
from .tasks import auto_post_blog

app = Celery('djmain')

app.conf.beat_schedule = {
    'post_blog_every_day': {
        'task': 'your_app.tasks.auto_post_blog',
        'schedule': crontab(minute=10, hour=0),  # Schedule for 10 minutes past midnight UTC
    },
}


class BlogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blogs'
