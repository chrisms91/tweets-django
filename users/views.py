from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import User
from .serializer import UserSerializer
from tweets.serializer import TweetSerializer


# Create your views here.
@api_view(["GET"])
def user(request, user_id):
    try:
        curr_user = User.objects.get(pk=user_id)
        tweets_from_curr_user = curr_user.tweet_set.all()
        serializers = TweetSerializer(tweets_from_curr_user, many=True)
        return Response(serializers.data)
    except User.DoesNotExist:
        raise NotFound
