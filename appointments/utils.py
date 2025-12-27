from datetime import date
from django.db.models import Max
from .models import Appointment

AVG_SERVICE_TIME = 5  # minutes per appointment


def generate_token(today=None):
    if today is None:
        today = date.today()

    last_token = Appointment.objects.filter(
        date=today
    ).aggregate(max_token=Max('token'))['max_token']

    if last_token is None:
        return 1

    return last_token + 1


def calculate_estimated_wait():
    today = date.today()

    waiting_count = Appointment.objects.filter(
        date=today,
        status='waiting'
    ).count()

    return waiting_count * AVG_SERVICE_TIME
