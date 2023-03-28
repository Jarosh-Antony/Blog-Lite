import blog_app_lite
from celery import Celery

app = Celery('tasks',include=['blog_app_lite.async_jobs.tasks'])
app.conf.update(
    broker_url = 'redis://localhost:6379/0',
    result_backend = 'redis://localhost:6379/1'
)