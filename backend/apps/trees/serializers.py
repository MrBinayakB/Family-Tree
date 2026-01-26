from rest_framework import serializers
from apps.trees.models import Trees
class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trees
        fields = '__all__'