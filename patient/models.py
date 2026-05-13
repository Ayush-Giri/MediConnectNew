from django.db import models
from django.contrib.auth import get_user_model
from insurance_provider.models import InsuranceProvider

# Create your models here.

User = get_user_model()


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="patient_profile")
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=5)
    allergies = models.TextField()
    chronic_conditions = models.TextField()
    insurance_provider = models.ForeignKey(InsuranceProvider, on_delete=models.SET_NULL, null=True)
    emergency_contact = models.BigIntegerField()







