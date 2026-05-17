from django.shortcuts import render
from email_verification.models import EmailVerification
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model


# Create your views here.

User = get_user_model()

class VerifyEmail(APIView):
    def get(self, request, link):
        # browser by default sends a get request
        instance = get_object_or_404(EmailVerification, link=link)
        instance.is_used = True
        instance.save()
        user_instance = User.objects.get(id=instance.user.id)
        user_instance.is_email_verified = True
        user_instance.save()
        return Response(
            {"message": "email verified successfully"},
            status=status.HTTP_200_OK
        )



