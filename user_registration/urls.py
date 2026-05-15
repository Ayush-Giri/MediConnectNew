from django.urls import path
from user_registration.views import UserRegistrationView, SendForgotPasswordEmailOtp


urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('send-email-otp/', SendForgotPasswordEmailOtp.as_view()),
    # path('deactivate-user/'),
]