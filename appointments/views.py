from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date

from .models import Appointment
from .serializers import AppointmentSerializer
from .utils import generate_token


# -----------------------------
# 1️⃣ Book Appointment
# -----------------------------
@api_view(['POST'])
def book_appointment(request):
    data = request.data

    appointment = Appointment.objects.create(
        name=data.get('name'),
        phone=data.get('phone'),
        date=data.get('date'),
        time_slot=data.get('time_slot'),
        token=generate_token(),
        status='waiting'
    )

    return Response({
        "message": "Appointment booked successfully",
        "appointment": AppointmentSerializer(appointment).data
    })


# -----------------------------
# 2️⃣ Queue Status
# -----------------------------
@api_view(['GET'])
def queue_status(request):
    today = date.today()

    queue = Appointment.objects.filter(
        date=today,
        status='waiting'
    ).order_by('created_at')

    current = Appointment.objects.filter(
        date=today,
        status='serving'
    ).first()

    return Response({
        "current_token": current.token if current else None,
        "queue": AppointmentSerializer(queue, many=True).data
    })


# -----------------------------
# 3️⃣ Call Next Token
# -----------------------------
@api_view(['POST'])
def call_next(request):
    today = date.today()

    # Complete current serving
    current = Appointment.objects.filter(
        date=today,
        status='serving'
    ).first()

    if current:
        current.status = 'completed'
        current.save()

    # Serve next waiting
    next_appt = Appointment.objects.filter(
        date=today,
        status='waiting'
    ).order_by('created_at').first()

    if next_appt:
        next_appt.status = 'serving'
        next_appt.save()
        return Response({
            "message": f"Token {next_appt.token} is now being served"
        })

    return Response({
        "message": "No appointments left in queue"
    })


# -----------------------------
# 4️⃣ Add Delay (Admin)
# -----------------------------
@api_view(['POST'])
def add_delay(request):
    delay = int(request.data.get('delay', 0))

    return Response({
        "message": f"Delay of {delay} minutes applied to queue",
        "delay_added": delay
    })
