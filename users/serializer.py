from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):

    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=20)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
