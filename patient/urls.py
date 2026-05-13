from django.urls import path
from patient.views import PatientView

urlpatterns = [
    path('', PatientView.as_view()),
    path('<int:id>/', PatientView.as_view()),
]