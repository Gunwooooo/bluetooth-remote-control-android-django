from rest_framework import serializers
from .models import HospitalInfo, PharmacyInfo

class HospitalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalInfo
        fields = '__all__'

class PharmacyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyInfo
        fields = '__all__'
