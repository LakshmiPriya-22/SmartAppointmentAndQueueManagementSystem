from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date

from .models import Appointment
from .serializers import AppointmentSerializer
from .utils import generate_token, calculate_estimated_wait


# -----------------------------
# 1️⃣ Book Appointment
# -----------------------------
@api_view(['POST'])
def book_appointment(request):
    data = request.data

    estimated_wait = calculate_estimated_wait()

    appointment = Appointment.objects.create(
        name=data.get('name'),
        phone=data.get('phone'),
        date=data.get('date'),
        time_slot=data.get('time_slot'),
        token=generate_token(),
        status='waiting',
        estimated_wait=estimated_wait
    )

    return Response({
        "message": "Appointment booked successfully",
        "token": appointment.token,
        "estimated_wait": estimated_wait
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

    # Complete current
    current = Appointment.objects.filter(
        date=today,
        status='serving'
    ).first()

    if current:
        current.status = 'completed'
        current.save()

    # Serve next
    next_appt = Appointment.objects.filter(
        date=today,
        status='waiting'
    ).order_by('created_at').first()

    if next_appt:
        next_appt.status = 'serving'
        next_appt.estimated_wait = 0
        next_appt.save()

        # Update wait for remaining queue
        queue = Appointment.objects.filter(
            date=today,
            status='waiting'
        ).order_by('created_at')

        for index, appt in enumerate(queue):
            appt.estimated_wait = (index + 1) * 5
            appt.save()

        return Response({
            "message": f"Token {next_appt.token} is now being served"
        })

    return Response({
        "message": "No appointments left"
    })


# -----------------------------
# 4️⃣ Add Delay (Admin)
# -----------------------------
@api_view(['POST'])
def add_delay(request):
    delay = int(request.data.get('delay', 0))
    today = date.today()

    queue = Appointment.objects.filter(
        date=today,
        status='waiting'
    ).order_by('created_at')

    for appt in queue:
        appt.estimated_wait += delay
        appt.save()

    return Response({
        "message": f"Delay of {delay} minutes applied",
        "delay_added": delay
    })
