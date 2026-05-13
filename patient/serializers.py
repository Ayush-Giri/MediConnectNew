from rest_framework import serializers
from patient.models import Patient

    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_image = models.ImageField(upload_to="patient_profile")
    # date_of_birth = models.DateField()
    # blood_group = models.CharField(max_length=5)
    # allergies = models.TextField()
    # chronic_conditions = models.TextField()
    # insurance_provider = models.ForeignKey(InsuranceProvider, on_delete=models.SET_NULL, null=True)
    # emergency_contact = models.BigIntegerField()



class PatientSerializer(serializers.ModelSerializer):
    insurance_provider_detail = serializers.SerializerMethodField()
    class Meta:
        model = Patient
        fields = [
            'id',
            'user',
            'profile_image',
            'date_of_birth',
            'blood_group',
            'allergies',
            'chronic_conditions',
            'insurance_provider',
            'insurance_provider_detail',
            'emergency_contact',
        ]
        read_only_fields = [
            'insurance_provider_detail'
        ]


    def get_insurance_provider_detail(self, obj):
        # object is the model instance for this model
        return f"{obj.insurance_provider.name} {obj.insurance_provider.contact}"
