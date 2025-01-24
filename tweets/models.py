from django.db import models

# Create your models here.
class Tweet(models.Model):
    """
    payload: Text(max. lenght 180)
    user: ForeignKey
    created_at: Date
    updated_at: Date
    """

    payload = models.TextField(max_length=180)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.payload[:20]}"
    

class Like(models.Model):
    """
    user: ForeignKey
    tweet: ForeignKey
    created_at: Date
    updated_at: Date
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    tweet = models.ForeignKey('tweets.Tweet', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user} likes this Tweet: {self.tweet.id}"