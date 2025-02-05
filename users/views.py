from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import User
from .serializer import UserSerializer, TinyUserSerializer

from tweets.serializer import TweetSerializer


class Users(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_users = User.objects.all()
        serializers = TinyUserSerializer(all_users, many=True)
        return Response(serializers.data)

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            new_user.set_password(password)
            new_user.save()
            serializer = UserSerializer(new_user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_pwd = request.data.get("old_password")
        new_pwd = request.data.get("new_password")
        if user.check_password(old_pwd):
            user.set_password(new_pwd)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, user_id):
        curr_user = self.get_object(user_id)
        serializers = UserSerializer(curr_user)
        return Response(serializers.data)


class UserTweets(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, user_id):
        curr_user = self.get_object(user_id)
        tweets_from_user = curr_user.tweet_set.all()
        serializers = TweetSerializer(tweets_from_user, many=True)
        return Response(serializers.data)


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"ok": "welcome"})
        else:
            return Response({"error": "wrong password"})


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "byee"})
