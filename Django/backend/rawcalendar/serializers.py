from rest_framework import serializers
from .models import RawCalendar

class RawCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawCalendar
        fields = '__all__'
