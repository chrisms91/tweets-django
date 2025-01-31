from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from .serializer import TweetSerializer
from .models import Tweet


class Tweets(APIView):

    def get(self, request):
        all_tweets = Tweet.objects.all()
        serializers = TweetSerializer(all_tweets, many=True)
        return Response(serializers.data)


class TweetDetail(APIView):

    def get_object(self, tweet_id):
        try:
            tweet = Tweet.objects.get(pk=tweet_id)
        except Tweet.DoesNotExist:
            raise NotFound
        return tweet

    def get(self, request, tweet_id):
        serializers = TweetSerializer(self.get_object(tweet_id))
        return Response(serializers.data)


# # Create your views here.
# def get_all_tweets(request):
#     tweets = Tweet.objects.all()
#     return render(
#         request,
#         "all_tweets.html",
#         {"tweets": tweets},
#     )


# @api_view(["GET"])
# def tweets(request):
# all_tweets = Tweet.objects.all()
# serializers = TweetSerializer(all_tweets, many=True)
# return Response(serializers.data)
