from django.urls import path
from . import views


urlpatterns = [
    path("", views.Users.as_view()),
    path("password", views.ChangePassword.as_view()),
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
    path("<int:user_id>", views.UserDetail.as_view()),
    path("<int:user_id>/tweets", views.UserTweets.as_view()),
]
