from django.urls import path
from user_registration.views import UserRegistrationView, SendForgotPasswordEmailOtp, deactive_user, VerifyPhoneNumber, send_email_verification_link, MeView


urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('verify-phone/', VerifyPhoneNumber.as_view()),
    path('send-email-verification-link/', send_email_verification_link),
    path('send-email-otp/', SendForgotPasswordEmailOtp.as_view()),
    path('deactivate-user/', deactive_user),
    path('me/', MeView.as_view())
]