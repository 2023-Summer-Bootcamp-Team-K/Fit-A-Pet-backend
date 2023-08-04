from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Pet

@registry.register_document
class PetDocument(Document):
    class Index:
        name = 'pets'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Pet
        fields = [
            'name',
            'age',
            'species',
            'gender',
            'weight',
            'started_date',
            'feed',
            'sore_spot',
            'profile_url',
            'profile_image',
            'created_at',
            'updated_at',
            'is_deleted',
        ]