from rest_framework import serializers
from apps.users.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("username", "email", "password")  # username required

    def create(self, validated_data):
        # create_user expects username and password
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"]
        )
        return user