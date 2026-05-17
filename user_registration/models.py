from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class RoleChoices(models.TextChoices):
    patient = ('patient', 'Patient')
    doctor = ('doctor', 'Doctor')
    clinic_admin = ("clinic admin", "Clinic Admin")

class CustomUser(AbstractUser):
    role = models.CharField(choices=RoleChoices.choices, max_length=50, blank=True)
    forgot_password_email_otp = models.CharField(null=True, unique=True, max_length=10, blank=True)
    forgot_password_phone_otp = models.CharField(null=True, unique=True, max_length=10, blank=True)
    phone_number = models.CharField(max_length=20, null=True, unique=True, blank=True)
    phone_verification_otp = models.CharField(null=True, max_length=10, blank=True)
    is_email_verified = models.BooleanField(default=False, blank=True)
    is_phone_verified = models.BooleanField(default=False, blank=True)
    is_account_verified = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
