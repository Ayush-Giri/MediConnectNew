from rest_framework.routers import DefaultRouter
from admin_control.views import VerifyDoctors
from django.urls import path , include

router = DefaultRouter()

router.register('verify-doctors',VerifyDoctors)

urlpatterns = [
    path('', include(router.urls))
]