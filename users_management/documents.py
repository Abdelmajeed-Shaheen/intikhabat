from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import ElasticUser

@registry.register_document
class VoterDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'voters'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = ElasticUser # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'elector_name',
            'circle_name',
            'election_place_name'
        ]
