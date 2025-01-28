from django.contrib import admin
from .models import Tweet, Like


class ElonFilter(admin.SimpleListFilter):

    title = "Elon Musk"
    parameter_name = "Elon"

    def lookups(self, request, model_admin):
        return [
            ("no elon musk", "No Elon Musk"),
            ("elon musk", "Elon Musk"),
        ]

    def queryset(self, request, tweets):
        param = self.value()
        filtered = tweets
        if param == "elon musk":
            filtered = filtered.filter(payload__contains="elon musk")
        elif param == "no elon musk":
            filtered = filtered.exclude(payload__contains="elon musk")
        return filtered


# Register your models here.
@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "payload",
        "total_likes",
        "created_at",
        "updated_at",
    )

    def total_likes(self, tweet):
        return tweet.likes.all().count()

    search_fields = (
        "payload",
        "user__username",
    )

    list_filter = (
        ElonFilter,
        "created_at",
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "tweet",
        "created_at",
        "updated_at",
    )

    search_fields = ("user__username",)

    list_filter = ("created_at",)
