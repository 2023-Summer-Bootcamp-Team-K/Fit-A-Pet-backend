from rest_framework import serializers
from .models import Meat, Oil, Supplement


class MeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meat
        fields = ['name', 'description', 'image_url']


class OilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oil
        fields = ['name', 'description', 'image_url']


class SupplementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplement
        fields = ['name', 'description', 'image_url']
