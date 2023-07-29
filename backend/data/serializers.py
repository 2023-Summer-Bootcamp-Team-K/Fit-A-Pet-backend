from rest_framework import serializers
from .models import Data


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('timestamp', 'bloodsugar')