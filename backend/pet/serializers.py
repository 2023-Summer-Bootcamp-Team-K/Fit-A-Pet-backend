from rest_framework import serializers
from .models import Pet

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ('user', 'name', 'age', 'species', 'gender', 'weight',
                  'started_date', 'feed', 'sore_spot', 'profile_url')
