from django.db import models
from common.models import CommonModel


# Create your models here.
class Tweet(CommonModel):
    """
    payload: Text(max. lenght 180)
    user: ForeignKey
    created_at: Date
    updated_at: Date
    """

    payload = models.TextField(max_length=180)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.payload


class Like(CommonModel):
    """
    user: ForeignKey
    tweet: ForeignKey
    created_at: Date
    updated_at: Date
    """

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    tweet = models.ForeignKey(
        "tweets.Tweet",
        on_delete=models.CASCADE,
        related_name="likes",
    )

    def __str__(self):
        return f"{self.tweet.payload}"
