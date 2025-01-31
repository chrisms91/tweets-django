from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.Tweets.as_view()),
    path("<int:tweet_id>", views.TweetDetail.as_view()),
]
