from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin, ListModelMixin
from rest_framework import permissions
from user_registration.models import CustomUser
from user_registration.serializers import UserRegistrationSerializer
from pagination import BasePagination

# Create your views here.


class VerifyDoctors(UpdateModelMixin, ListModelMixin, GenericViewSet):
    queryset = CustomUser.objects.filter(role="doctor", is_account_verified=False)
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = BasePagination