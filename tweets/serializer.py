from rest_framework import serializers
from .models import Tweet


class TweetSerializer(serializers.Serializer):

    pk = serializers.IntegerField(read_only=True)
    payload = serializers.CharField(max_length=180)
