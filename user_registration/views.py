from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from user_registration.serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model
from throttle import SignUpThrottle, VerifyPhoneNumberThrottle
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from helpers import generate_mc_otp
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.

User = get_user_model()


class UserRegistrationView(CreateAPIView):
    # phone number verification should happen again if the user updates his phone number
    serializer_class = UserRegistrationSerializer
    throttle_classes = [SignUpThrottle]


class VerifyPhoneNumber(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [VerifyPhoneNumberThrottle]

    def get(self, request):
        # use get to generate otp and set it into user table
        user_instance = request.user
        user_instance.phone_verification_otp = generate_mc_otp()
        user_instance.save()
        return Response(
            {"message": "An otp code has been successfully sent to your device"},
            status=status.HTTP_200_OK
        )
    

    def post(self, request):
        # use post request to get the otp and verify it
        otp = request.data.get('otp')
        user_instance = request.user
        if user_instance.phone_verification_otp is None:
            return Response(
                {"message": "otp has not been generated yet"},
                status=status.HTTP_204_NO_CONTENT
            )
        if otp == user_instance.phone_verification_otp:
            user_instance.phone_verification_otp = None
            user_instance.is_phone_verified = True
            user_instance.save()
            return Response(
                {"message": "phone number verified successfully"},
                status=status.HTTP_200_OK
            )
        else:
            user_instance.phone_number = None
            user_instance.save()
            return Response(
                {"message": "otp incorrect please generate a new otp and try again"},
                ststus=status.HTTP_400_BAD_REQUEST
            )


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def deactive_user(request):
    if request.method == "GET":
        user = request.user
        user.is_active = False
        user.save()
        return Response(
            {"message": "user deactivated successully"},
            status=status.HTTP_200_OK
        )
    elif request.method == "POST":
        user = request.user
        user.is_active = False
        user.save()
        return Response(
            {"message": "user deactivated successully"},
            status=status.HTTP_200_OK
        )
        

class SendForgotPasswordEmailOtp(APIView):
    def post(self, request):
        email = request.data.get('email')
        user_instance = get_object_or_404(User, email=email)
        if user_instance.is_email_verified:
            otp = generate_mc_otp()
            user_instance.forgot_password_email_otp = otp
            user_instance.save()

            return Response(
                {"message": "email sent successfully"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "you have not verified your email so password cant be reset"},
                status=status.HTTP_403_FORBIDDEN
            )


class SendForgotPasswordPhoneOtp(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        user_instance = get_object_or_404(User, phone_number=phone_number)
        if user_instance.is_phone_verified:
            otp = generate_mc_otp()
            user_instance.forgot_password_phone_otp = otp
            user_instance.save()
        else:
            return Response(
                {"message": "you have not verified your phone number password cannot be reset"},
                status=status.HTTP_400_BAD_REQUEST
            )








