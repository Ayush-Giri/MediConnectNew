from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin, ListModelMixin
from rest_framework import permissions
from user_registration.models import CustomUser
from .serializers import VerfiyDoctorSerializer
from pagination import BasePagination
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

# Create your views here.


class VerifyDoctors(UpdateModelMixin, ListModelMixin, GenericViewSet):
    queryset = CustomUser.objects.filter(role="doctor", is_account_verified=False)
    serializer_class = VerfiyDoctorSerializer
    # permission_classes = [permissions.IsAdminUser]
    pagination_class = BasePagination
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]