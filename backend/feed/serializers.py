from rest_framework import serializers
from .models import Meat, Oil, Supplement


class MeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meat
        fields = ['name']


class OilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oil
        fields = ['name']


class SupplementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplement
        fields = ['name']
