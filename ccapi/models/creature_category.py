from django.db import models
from .creature import Creature
from .category import Category

class CreatureCategory(models.Model):
    creature = models.ForeignKey(Creature, on_delete=models.CASCADE, related_name='category')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='creature')
