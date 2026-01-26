from rest_framework import serializers
from apps.relationship.models import Relation
class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = '__all__'