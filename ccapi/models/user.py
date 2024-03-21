from django.db import models

class User(models.Model):
    uid = models.CharField(max_length=50)
    name = models.CharField(max_length=20, default="User")
    bio = models.CharField(max_length=500, default="No bio provided")
