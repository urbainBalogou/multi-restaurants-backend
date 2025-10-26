import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multi_restaurants.settings')

app = Celery('multi_restaurants')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Periodic tasks
app.conf.beat_schedule = {
    'cleanup-expired-coupons': {
        'task': 'apps.promotions.tasks.cleanup_expired_coupons',
        'schedule': crontab(hour=0, minute=0),  # Every day at midnight
    },
    'send-daily-stats': {
        'task': 'apps.commandes.tasks.send_daily_stats_email',
        'schedule': crontab(hour=8, minute=0),  # Every day at 8 AM
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
