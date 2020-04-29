from __future__ import absolute_import, unicode_literals
from celery import shared_task
import datetime
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from main import models


@shared_task(name='check_promotions')
def check_promotion():
    all_promotions = models.Promotion.objects.all()

    return [promotion.delete() for promotion in all_promotions
     if promotion.end_date < datetime.datetime.now().date()]


schedule, created = IntervalSchedule.objects.get_or_create(
    every=10,
    period=IntervalSchedule.SECONDS
)

PeriodicTask.objects.get_or_create(
    interval=schedule,
    task='check_promotions',
    name='Check promotions by delete'
)

