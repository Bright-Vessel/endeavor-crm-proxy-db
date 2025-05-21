from rest_framework import serializers
from apps.proxy.models import AvailabilitySlot


class AvailabilitySlotSerializer(serializers.ModelSerializer):
    start_datetime = serializers.CharField(source='start_datetime_raw')
    end_datetime = serializers.CharField(source='end_datetime_raw')

    class Meta:
        model = AvailabilitySlot
        fields = ('start_datetime', 'end_datetime', 'is_available', 'length')
