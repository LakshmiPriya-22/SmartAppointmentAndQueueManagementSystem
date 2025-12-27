from django.db import models

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('serving', 'Serving'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time_slot = models.CharField(max_length=20)
    token = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')
    estimated_wait = models.IntegerField(default=0)  # minutes
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
