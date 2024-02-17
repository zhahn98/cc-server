from django.db import models
from .user import User
from .rarity import Rarity

class Creature(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    lore = models.CharField(max_length=250)
    img = models.URLField()
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE, default=1)
