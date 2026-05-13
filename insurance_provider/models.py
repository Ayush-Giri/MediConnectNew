from django.db import models

# Create your models here.

class InsuranceProvider(models.Model):
    name = models.CharField(max_length=100)
    contact = models.BigIntegerField()


    def __str__(self):
        f"{self.name} | {self.contact}"

