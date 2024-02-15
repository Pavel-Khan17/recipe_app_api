from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPE_URL = reverse('recipe:recipe-list')

def sample_recipe(user, **parems):
  """ Create and return sample recipe object"""
  defaults = {
    'title' : "Briyani",
    'time_minutes' : 30,
    'price' : 5.00,
  }
  defaults.update(parems)
  
  return Recipe.objects.create(user=user, **defaults)

def sample_user(email='test@example.com', password='test1234'):
  """ Create and return sample user object"""
  return get_user_model().objects.create_user(email=email,password=password)


class PublicRecipeApiTest(TestCase):
  """ Test unauthenticated recipe API access """
  
  def setUp(self):
    self.client = APIClient()
  
  
  def test_authenticated_required(self):
    """ test the authentication is required """
    res = self.client.get(RECIPE_URL)
    
    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
  """ Test authenticated recipe API access """
  
  def setUp(self):
    self.user = sample_user()
    self.client = APIClient()
    self.client.force_authenticate(self.user)
  
  
  def test_retrieve_recipes_list(self):
    """ Test retrieving recipe list successfuly """
    sample_recipe(user=self.user)
    sample_recipe(user=self.user)
    
    res = self.client.get(RECIPE_URL)
    
    recipes = Recipe.objects.all().order_by('id')
    serializer = RecipeSerializer(recipes, many=True)
    
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)
  
  
  def test_recipes_limited_to_user(self):
    """ test retrieving recipes for user """
    user2 = sample_user(
      email='other@example.com',
      password='password1234'
    )
    sample_recipe(user=user2)
    sample_recipe(user=self.user)
    
    res = self.client.get(RECIPE_URL)
    
    recipes = Recipe.objects.filter(user=self.user)
    serializer = RecipeSerializer(recipes, many=True)
    
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(len(res.data), 1)
    self.assertEqual(res.data, serializer.data)
