import os

from celery import Celery
from decouple import config

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "minitwitter.settings",
)


def get_broker_url():
    service = config("CELERY_BROKER_SERVICE")
    host = config("CELERY_BROKER_HOST")
    port = config("CELERY_BROKER_PORT")
    broker_url = f"{service}://{host}:{port}/0"
    return broker_url


class CeleryConfig:
    broker_url = get_broker_url()
    task_always_eager = False
    task_eager_propagates = False


app = Celery("minitwitter")
app.config_from_object(CeleryConfig())
app.autodiscover_tasks()
