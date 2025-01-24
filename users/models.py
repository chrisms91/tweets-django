from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=150, editable=True)
    last_name = models.CharField(max_length=150, editable=True)
    name = models.CharField(max_length=150, default="")
    email = models.CharField(max_length=20, default="")