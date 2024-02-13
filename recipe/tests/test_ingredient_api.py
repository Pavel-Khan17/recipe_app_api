from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse('recipe:ingredient-list')

def sample_user(email='test@example.com', password='test1234'):
  """ Creating sample user """
  return get_user_model().objects.create_user(email, password)


class PublicIngredientApiTest(TestCase):
  """ test the public available api for ingredient """
  
  def setUp(self):
    self.client = APIClient()
  
  def test_login_required(self):
    """ test that loging is required for retreving ingradient """
    
    res = self.client.get(INGREDIENT_URL)
    
    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):
  """ test the ingredient api for authenticated users """
  
  def setUp(self):
    self.user = sample_user()
    
    self.client = APIClient()
    self.client.force_authenticate(self.user)
  
  
  def test_retrieve_ingredient(self):
    """ test retrieving ingredient successfuly"""
    Ingredient.objects.create(user = self.user, name= 'cucamber')
    Ingredient.objects.create(user = self.user, name= 'black pepper')
    
    res = self.client.get(INGREDIENT_URL)
    
    ingredients = Ingredient.objects.all()
    serializer = IngredientSerializer(ingredients, many=True)
    
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)
  
  
  def test_ingredient_limited_to_user(self):
    """ test that ingredient limited to the creator user only """
    user2 = sample_user(email="user2@example.com", password="user21234")
    
    Ingredient.objects.create(user = user2, name = 'black pepper')
    ingredient = Ingredient.objects.create(user = self.user, name = 'cucumber')
    
    res = self.client.get(INGREDIENT_URL)
    
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(len(res.data), 1)
    self.assertEqual(res.data[0]['name'], ingredient.name)
  
  
  def test_create_ingredient_successfuly(self):
    """ test that ingredient is created successfully"""
    payload = {'name':'cucumber'}
    
    res = self.client.post(INGREDIENT_URL, payload)
    
    exists = Ingredient.objects.filter(
      user = self.user,
      name = payload['name']
    ).exists()
    
    self.assertTrue(exists)
  
  
  def test_create_ingredient_invalid(self):
    """ test creating ingredient with invalid payload """
    payload = {'name': ''}
    
    res = self.client.post(INGREDIENT_URL, payload)
    
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)