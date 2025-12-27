from .models import Appointment

def generate_token():
    last = Appointment.objects.order_by('-id').first()
    if last:
        number = int(last.token[1:]) + 1
    else:
        number = 1
    return f"A{number}"
