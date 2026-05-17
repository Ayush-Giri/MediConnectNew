from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, null=True)
    link = models.CharField(max_length=25)
    is_used = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username} | {self.email}"

