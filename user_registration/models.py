from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class RoleChoices(models.TextChoices):
    patient = ('patient', 'Patient')
    doctor = ('doctor', 'Doctor')
    clinic_admin = ("clinic admin", "Clinic Admin")

class CustomUser(AbstractUser):
    role = models.CharField(choices=RoleChoices.choices, max_length=50)
    forgot_password_email_otp = models.CharField(null=True, unique=True, max_length=10)
    forgot_password_phone_otp = models.CharField(null=True, unique=True, max_length=10)
    phone_number = models.BigIntegerField(null=True, unique=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_account_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        if self.role == "doctor":
            self.is_account_verified = False
        super().save(*args, **kwargs)
