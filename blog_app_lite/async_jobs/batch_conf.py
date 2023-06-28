broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/1'

# from datetime import time

# CELERY_IMPORTS = ('tasks',)
# CELERY_TIMEZONE = 'UTC'
# CELERY_ENABLE_UTC = True

# CELERYBEAT_SCHEDULE = {
    # 'my-task-every-day': {
        # 'task': 'tasks.dailyPDF',
        # 'schedule': time(hour=22, minute=43),
    # },
# }