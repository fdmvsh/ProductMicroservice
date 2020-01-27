from celery import Celery
from celery.schedules import crontab

from micro import get_offers_all
import config

celery = Celery()
celery.config_from_object(config)


@celery.task(name="periodic_task")
def periodic_task():
    print("Getting offers from Offers MS...")
    get_offers_all()
