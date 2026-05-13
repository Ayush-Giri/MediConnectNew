from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from patient.serializers import PatientSerializer
from patient.models import Patient
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView

# Create your views here.

class PatientView(CreateAPIView, RetrieveAPIView, UpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


