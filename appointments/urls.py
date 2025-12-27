from django.urls import path
from .views import (
    book_appointment,
    queue_status,
    call_next,
    add_delay
)

urlpatterns = [
    path('book/', book_appointment),
    path('queue/', queue_status),
    path('next/', call_next),
    path('delay/', add_delay),
]
