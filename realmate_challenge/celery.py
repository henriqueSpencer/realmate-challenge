import os
from celery import Celery

# Set the Django settings environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realmate_challenge.settings')

# Initialize Celery
celery_app = Celery('realmate_challenge')

# Load Django configurations
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in Django apps
celery_app.autodiscover_tasks()
