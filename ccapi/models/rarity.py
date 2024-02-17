from django.db import models

class Rarity(models.Model):
    label = models.CharField(max_length=50)
