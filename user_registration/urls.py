from django.urls import path
from user_registration.views import UserRegistrationView, SendForgotPasswordEmailOtp, deactive_user, VerifyPhoneNumber


urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('verify-phone/', VerifyPhoneNumber.as_view()),
    path('send-email-otp/', SendForgotPasswordEmailOtp.as_view()),
    path('deactivate-user/', deactive_user),
]