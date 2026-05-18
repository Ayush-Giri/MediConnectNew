from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView
from user_registration.serializers import UserRegistrationSerializer, MeSerializer
from django.contrib.auth import get_user_model
from throttle import SignUpThrottle, VerifyPhoneNumberThrottle, VerifyEmailThrottle, ChangePasswordDailyThrottle, ChangePasswordHourlyThrottle, ForgotPasswordDailyThrottle, ForgotPasswordHourlyThrottle
from rest_framework.views import APIView
from helpers import generate_mc_otp, generate_email_verification_url
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from email_verification.models import EmailVerification
import twilio_sms
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404

# Create your views here.

User = get_user_model()


class UserRegistrationView(CreateAPIView):
    # phone number verification should happen again if the user updates his phone number
    serializer_class = UserRegistrationSerializer
    throttle_classes = [SignUpThrottle]


class MeView(APIView):
    # if a user changes is phone number or email then they have to verify their email and phone number
    # again as it will be unverified
    permission_classes = [IsAuthenticated]
    serializer_class = MeSerializer

    def get(self, request):
        serializer = MeSerializer(request.user, context={"request": request})
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
    def patch(self, request):
        serializer = MeSerializer(request.user, data=request.data, context={"request": request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_200_OK
        )


class VerifyPhoneNumber(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [VerifyPhoneNumberThrottle]

    def get(self, request):
        # use get to generate otp and set it into user table
        user_instance = request.user
        generated_otp = generate_mc_otp()
        user_instance.phone_verification_otp = generated_otp
        user_instance.save()
        # twilio_sms.send_sms(user_phone_number=user_instance.phone_number, otp=generated_otp)
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
@throttle_classes([VerifyEmailThrottle])
def send_email_verification_link(request):
    if request.method == "GET":
        EmailVerification.objects.create(user=request.user, link=generate_email_verification_url(), email=request.user.email)
        return Response(
            {"message": "a verification link has been sent to you email"},
            status=status.HTTP_200_OK
        )
    elif request.method == "POST":
        EmailVerification.objects.create(user=request.user, link=generate_email_verification_url())
        return Response(
            {"message": "a verification link has been sent to you email"},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED
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
    else:
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class ChangePassword(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRegistrationSerializer
    throttle_classes = [ChangePasswordHourlyThrottle, ChangePasswordDailyThrottle]
    queryset = User.objects.all()
    lookup_field = "id"

    def partial_update(self, request, *args, **kwargs):
        user_instance = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get("new_password")
        if user_instance.check_password(old_password):
            user_instance.set_password(new_password)
            user_instance.save()
            return Response(
                {"message": "password changed successfully"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )


# forgot password implementation here give option for both email and phone number based

class ForgotPassword(APIView):
    # throttle_classes = [ForgotPasswordHourlyThrottle, ForgotPasswordDailyThrottle]

    def get(self, request):
        # first verify if the email or phone number exists or not if exist then send otp
        # else send response that email or phone_number does not exist
        medium = request.query_params.get('medium')
        credential = request.query_params.get('credential')

        if medium == "email":
            try:
                user_instance = User.objects.get(email=credential)
                generated_otp = generate_mc_otp()
                user_instance.forgot_password_email_otp = generate_mc_otp()
                user_instance.save()
                return Response(
                    {"message": "an email with otp as been sent to you email"},
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    {"message": "no such email exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif medium == "phone":
            prefixed_phone = "+977" + str(credential).strip()
        
            user_instance = get_object_or_404(User, phone_number=prefixed_phone)
            generated_otp = generate_mc_otp()
            user_instance.forgot_password_phone_otp = generated_otp
            user_instance.save()
            return Response(
                {"message": "an otp has been sent to your phone"},
                status=status.HTTP_200_OK
            )
            
        else:
            return Response(
                {"message": "enter a valid medium"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    
    def post(self, request):
        otp = request.data.get('otp')
        medium = request.data.get('medium')
        credential = request.data.get('credential')
        password = request.data.get('password')

        if medium == "phone":
            prefixed_phone = "+977" + str(credential).strip()
            try:
                user_instance = User.objects.get(phone_number=prefixed_phone)
                if user_instance.forgot_password_phone_otp == otp:
                    user_instance.set_password(password)
                    user_instance.forgot_password_phone_otp = None
                    user_instance.save()
                    return Response(
                        {"message": "password changed successfully"},
                        status=status.HTTP_200_OK
                    )
                else:
                    user_instance.forgot_password_phone_otp = None
                    user_instance.save()
                    return Response(
                        {"message": "the opt provided is incorrect generate a new otp again"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except User.DoesNotExist:
                return Response(
                    {"message": "the phone number provided is incorrect"}
                )
        elif medium == "email":
            user_instance = get_object_or_404(User, email=credential)
            if user_instance.forgot_password_email_otp == otp:
                user_instance.set_password(password)
                user_instance.forgot_password_email_otp = None
                user_instance.save()
                return Response(
                    {"message": "password changed successfully"},
                    status=status.HTTP_200_OK
                )
            else:
                user_instance.forgot_password_email_otp = None
                user_instance.save()
                return Response(
                        {"message": "the opt provided is incorrect generate a new otp again"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            return Response(
                {"message": "invalid medium"},
                status=status.HTTP_400_BAD_REQUEST
            )


