from django.contrib import admin
from .models import Tweet, Like


# Register your models here.
@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):

    list_display = ("user", "payload", "total_likes")

    def total_likes(self, tweet):
        return tweet.likes.all().count()


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
