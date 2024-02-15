from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
  """ Manage tags in the database """
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  queryset = Tag.objects.all()
  serializer_class = serializers.TagSerializer
  
  def get_queryset(self):
    """ return object for the current authenticated user only """
    return self.queryset.filter(user=self.request.user).order_by('-name')
  
  def perform_create(self, serializer):
    """ Create a new tag"""
    return serializer.save(user = self.request.user)

class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
  """ Manage Ingredient in the database """
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  queryset = Ingredient.objects.all()
  serializer_class = serializers.IngredientSerializer
  
  def get_queryset(self):
    """ return object for the current authenticated user only """
    return self.queryset.filter(user=self.request.user).order_by('-name')
  
  def perform_create(self, serializer):
    """ Create a new tag"""
    return serializer.save(user = self.request.user)

class RecipeViewSet(viewsets.ModelViewSet):
  """ Manage Recipe in the database """
  queryset = Recipe.objects.all()
  serializer_class = serializers.RecipeSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  
  def get_queryset(self):
    """ return object for the current authenticated user only """
    return self.queryset.filter(user=self.request.user)
  
  def get_serializer_class(self):
    """ return appropiate serializer class for different action """
    if self.action == 'retrieve':
      return serializers.RecipeDetailSerializer
    
    return self.serializer_class