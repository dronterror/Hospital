import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_website.settings')

app = Celery('hospital_website')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'send-appointment-reminders': {
        'task': 'apps.appointments.tasks.send_appointment_reminder',
        'schedule': crontab(hour=9, minute=0),  # Run daily at 9 AM
    },
    'cleanup-expired-appointments': {
        'task': 'apps.appointments.tasks.cleanup_expired_appointments',
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },
}

app.conf.timezone = 'UTC'

# Configure Celery
app.conf.update(
    broker_url=settings.CELERY_BROKER_URL,
    result_backend=settings.CELERY_RESULT_BACKEND,
    accept_content=['json'],
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    task_time_limit=600,  # 10 minutes
    task_soft_time_limit=300,  # 5 minutes
    broker_connection_retry_on_startup=True,
)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')