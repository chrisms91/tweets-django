from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from .models import User
from .serializer import UserSerializer

from tweets.serializer import TweetSerializer


class UserDetail(APIView):

    def get_object(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound
        return user

    def get(self, request, user_id):
        curr_user = self.get_object(user_id)
        tweets_from_user = curr_user.tweet_set.all()
        serializers = TweetSerializer(tweets_from_user, many=True)
        return Response(serializers.data)


# # Create your views here.
# @api_view(["GET"])
# def user(request, user_id):
#     try:
#         curr_user = User.objects.get(pk=user_id)
#         tweets_from_curr_user = curr_user.tweet_set.all()
#         serializers = TweetSerializer(tweets_from_curr_user, many=True)
#         return Response(serializers.data)
#     except User.DoesNotExist:
#         raise NotFound
