from rest_framework import serializers
from apps.people.models import People
class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = '__all__'