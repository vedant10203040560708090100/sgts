from django.db import models
import uuid

class Customer(models.Model):
    firm_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200)
    email = models.EmailField()
    activation_key = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    key_expires_at = models.DateTimeField()
    last_paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.firm_name

    def is_active(self):
        from django.utils import timezone
        return timezone.now() < self.key_expires_at
    