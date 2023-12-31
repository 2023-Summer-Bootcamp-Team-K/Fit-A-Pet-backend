from rest_framework import serializers
from .models import Pet


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ('id', 'name', 'age', 'species', 'gender', 'weight',
                  'started_date', 'feed', 'sore_spot', 'profile_image', 'profile_url')
