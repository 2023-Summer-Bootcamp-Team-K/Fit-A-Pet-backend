from rest_framework import serializers
from .models import Data


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = (
            'id', 'device', 'code', 'timestamp', 'record_type', 'bloodsugar', 'scan_bloodsugar')
