from rest_framework import serializers
from user_registration.models import CustomUser



class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'confirm_password',
            'role',
            'phone_number',
            'is_account_verified'
        ]

    
    def validate_username(self, data):
        if CustomUser.objects.filter(username=data).exists():
            raise serializers.ValidationError("User with username already exists")
        return data
    
    
    def validate_email(self, data):
        if CustomUser.objects.filter(email=data):
            raise serializers.ValidationError("Email already exists")
        return data
    
    def to_internal_value(self, data):
        data = data.copy()
        country_code = "+977"
        phone_number = data.get('phone_number')
        data['phone_number']  = country_code + phone_number
        if data["role"] == "doctor":
            data["is_account_verified"] = False
        return super().to_internal_value(data)


    def create(self, validated_data):
        if validated_data.get('password') != validated_data.get('confirm_password'):
            raise serializers.ValidationError("passowords do not match")
        validated_data.pop('confirm_password')
        return CustomUser.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        if validated_data.get('email'):
            instance.is_email_verified = False
            instance.save()
        if validated_data.get('phone_number'):
            instance.is_phone_verified = False
            instance.save()
        return instance
    

class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
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


    def validate_username(self, data):
        if CustomUser.objects.filter(username=data).exists():
            raise serializers.ValidationError("User with username already exists")
        return data
    
    
    def validate_email(self, data):
        if CustomUser.objects.filter(email=data):
            raise serializers.ValidationError("Email already exists")
        return data


    def create(self, validated_data):
        if validated_data.get('password') != validated_data.get('confirm_password'):
            raise serializers.ValidationError("passowords do not match")
        validated_data.pop('confirm_password')
        return CustomUser.objects.create_user(**validated_data)
    
    
    def update(self, instance, validated_data):
        if validated_data.get('email'):
            instance.is_email_verified = False
            instance.email = validated_data.get('email')
            instance.save()
        if validated_data.get('phone_number'):
            instance.is_phone_verified = False
            instance.phone_number = validated_data.get('phone_number')
            instance.save()
        return instance
    


    
