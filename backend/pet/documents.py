from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Pet

@registry.register_document
class PetDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'pets'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}


    class Django:
        model = Pet # The model associated with this Document
        # The fields of the model you want to be indexed in Elasticsearch
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
        ]
