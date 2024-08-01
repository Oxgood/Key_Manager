from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Access_key(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    date_of_procurement = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField()

    def check_expiry(self):
        if self.expiry_date and self.expiry_date < timezone.now():
            self.status = 'expired'
            self.save(update_fields=['status'])

    def __str__(self):
        return f"{self.pk} - {self.status}"
    


