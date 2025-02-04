from rest_framework.serializers import ModelSerializer
from .models import Tweet
from users.serializer import TinyUserSerializer


class TweetSerializer(ModelSerializer):

    class Meta:
        model = Tweet
        fields = (
            "id",
            "payload",
        )


class TweetDetailSerializer(ModelSerializer):

    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = "__all__"
