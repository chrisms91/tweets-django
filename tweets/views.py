from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Tweet
from .serializer import TweetSerializer


# Create your views here.
def get_all_tweets(request):
    tweets = Tweet.objects.all()
    return render(
        request,
        "all_tweets.html",
        {"tweets": tweets},
    )


@api_view(["GET"])
def tweets(request):
    all_tweets = Tweet.objects.all()
    serializers = TweetSerializer(all_tweets, many=True)
    return Response(serializers.data)
