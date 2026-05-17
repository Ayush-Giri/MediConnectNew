from django.urls import path, include
from email_verification.views import VerifyEmail

urlpatterns = [
    path('email/<str:link>/', VerifyEmail.as_view())
]