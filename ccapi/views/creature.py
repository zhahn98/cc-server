from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ccapi.models import Creature, User, CreatureCategory, Category, Rarity
from django.core.exceptions import ObjectDoesNotExist
import random
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
    
    # Get associated description of corresponding Rarity ID
    rarity_id = request.data["rarity"]
    rarity = Rarity.objects.get(pk=rarity_id)
    
    creature = Creature.objects.create(
      user = user,
      name = request.data["name"],
      img = request.data["imageUrl"],
      lore = request.data["lore"],
      rarity = rarity
    )
    
    creature.save()
    serializer = CreatureSerializer(creature)
    return Response(serializer.data)
  
  def update(self, request, pk):
    creature = Creature.objects.get(pk=pk)
    
    # Get associated description of corresponding Rarity ID
    rarity_id = request.data["rarity"]
    rarity = Rarity.objects.get(pk=rarity_id)
    
    creature.name = request.data["name"]
    creature.img = request.data["imageUrl"]
    creature.lore = request.data["lore"]
    creature.rarity = rarity
  
    creature.save()
    return Response(None, status=status.HTTP_200_OK)
  
  @action(methods=['post'], detail=True)
  def add_category_to_creature(self, request, pk):
      creature = Creature.objects.get(pk=pk)
      category = Category.objects.get(id=request.data['categoryId'])
      try:
        CreatureCategory.objects.get(creature=creature, category=category)
        return Response({'message: This creature already has this category.'})
      except CreatureCategory.DoesNotExist:
        CreatureCategory.objects.create(
            creature=creature,
            category=category
        )
        return Response(None, status=status.HTTP_200_OK)
  
  @action(methods=['delete'], detail=True)
  def remove_category_from_creature(self, request, pk):
      creature = Creature.objects.get(pk=pk)
      creature_category = CreatureCategory.objects.get(creature=creature, category=request.data['categoryId'])
      creature_category.delete()

      return Response(None, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    creature = Creature.objects.get(pk=pk)
    creature.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  @action(methods=['get'], detail=False)
  def random_creature(self, request):
        # Get all creatures
        all_creatures = Creature.objects.all()
        
        # Choose a random creature from all creatures
        random_creature = random.choice(all_creatures)
        
        # Serialize the random creature data
        serializer = CreatureSerializer(random_creature)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
