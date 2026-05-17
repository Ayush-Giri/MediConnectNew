from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class VerfiyDoctorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'phone_number',
            'is_account_verified',
            'is_email_verified',
            'is_phone_verified'
        ]
        read_only_fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'phone_number',
            'is_email_verified',
            'is_phone_verified',
        ]