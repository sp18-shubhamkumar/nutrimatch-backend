default_app_config = 'api.apps.ApiConfig'

from nutrimatch.celery import app as celery_app

__all__ = ('celery_app',)