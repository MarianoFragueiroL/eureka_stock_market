from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import ApiKey

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
            }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        ApiKey.objects.create(user=user)
        return user