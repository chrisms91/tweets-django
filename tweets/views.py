from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializer import TweetSerializer, TweetDetailSerializer
from .models import Tweet


class Tweets(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_tweets = Tweet.objects.all()
        serializers = TweetSerializer(all_tweets, many=True)
        return Response(serializers.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = TweetDetailSerializer(data=request.data)
            if serializer.is_valid():
                new_tweet = serializer.save(user=request.user)
                return Response(TweetDetailSerializer(new_tweet).data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class TweetDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, tweet_id):
        try:
            tweet = Tweet.objects.get(pk=tweet_id)
        except Tweet.DoesNotExist:
            raise NotFound
        return tweet

    def get(self, request, tweet_id):
        serializers = TweetDetailSerializer(self.get_object(tweet_id))
        return Response(serializers.data)

    def put(self, request, tweet_id):
        tweet = self.get_object(tweet_id)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if tweet.user != request.user:
            raise PermissionDenied

        serializer = TweetDetailSerializer(
            tweet,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            updated_tweet = serializer.save()
            return Response(TweetDetailSerializer(updated_tweet).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, tweet_id):
        tweet = self.get_object(tweet_id)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if tweet.user != request.user:
            raise PermissionDenied
        tweet.delete()
        return Response(status=HTTP_200_OK)
