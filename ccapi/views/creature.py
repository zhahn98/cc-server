from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ccapi.models import Creature, User, CreatureCategory, Category, Rarity

class CreatureView(ViewSet):
  
  def retrieve (self, request, pk):
    creature = Creature.objects.get(pk=pk)
    serializer = CreatureSerializer(creature)
    return Response(serializer.data)

  def list(self, request):
    creatures = Creature.objects.all()
    user = request.query_params.get('user', None)
    if user is not None:
      creatures = creatures.filter(user=user)
    serializer = CreatureSerializer(creatures, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def create(self, request):
    user = User.objects.get(pk=request.data["userId"])
    
    creature = Creature.objects.create(
      user = user,
      name = request.data["name"],
      img = request.data["imageUrl"],
      lore = request.data["lore"],
      rarity = request.data["rarity"]
    )
    
    creature.save()
    serializer = CreatureSerializer(creature)
    return Response(serializer.data)
  
  def update(self, request, pk):
    creature = Creature.objects.get(pk=pk)
    creature.name = request.data["name"],
    creature.img = request.data["imageUrl"],
    creature.lore = request.data["lore"],
    creature.rarity = request.data["rarity"]
  
    creature.save()
    return Response(None, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    creature = Creature.objects.get(pk=pk)
    creature.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)

class CreatureCategorySerializer(serializers.ModelSerializer):
  id = serializers.ReadOnlyField(source='category.id')
  label = serializers.ReadOnlyField(source='category.label')
  class Meta:
    model = CreatureCategory
    fields = ('id', 'label')

class CreatureSerializer(serializers.ModelSerializer):
  category = CreatureCategorySerializer(many=True, read_only=True)
  class Meta:
    model = Creature
    fields = ('id', 'user', 'name', 'img', 'lore', 'category', 'rarity')
    depth = 1
