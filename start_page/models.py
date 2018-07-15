from django.db import models


class User(models.Model):
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    email = models.EmailField()
    token = models.CharField(max_length=64)
    user_id = models.CharField(max_length=64)
