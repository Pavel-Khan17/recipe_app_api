from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient, Tag

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPE_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
  """ Return recipe details url """
  return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tag(user, name='Main Course'):
  """ Create and return sample Tags object """
  return Tag.objects.create(user=user, name=name)


def sample_ingredients(user, name='cucumber'):
  """ Create and return sample ingredients object"""
  return Ingredient.objects.create(user=user, name=name)


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
  
  
  def test_retrieve_recipe_detail(self):
    """ test retrieving recipe details """
    recipe = sample_recipe(user=self.user)
    recipe.tags.add(sample_tag(user=self.user))
    recipe.ingredients.add(sample_ingredients(user=self.user))
    
    url = detail_url(recipe.id)
    res = self.client.get(url)
    
    serializer = RecipeDetailSerializer(recipe)
    self.assertEqual(res.data, serializer.data)
  
  
  def test_create_basic_recipe(self):
    """ Test create recipe """
    payload = {
      'title' : 'Chocolates Cheesecake',
      'time_minutes' : 30,
      'price' : 6.00
    }
    
    res = self.client.post(RECIPE_URL, payload)
    
    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    recipe = Recipe.objects.get(id=res.data['id'])
    for key in payload.keys():
      self.assertEqual(payload[key], getattr(recipe, key))
  
  
  def test_create_recipe_with_tag(self):
    """ Test creating recipe with tags """
    tag1 = sample_tag(user=self.user, name='vegan')
    tag2 = sample_tag(user=self.user, name='Dessert')
    
    payload = {
      'title' : 'Chocolates Cheesecake',
      'time_minutes' : 30,
      'tags' : [tag1.id, tag2.id],
      'price' : 6.00
    }
    
    res = self.client.post(RECIPE_URL, payload)
    
    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    recipe = Recipe.objects.get(id=res.data['id'])
    tags = recipe.tags.all()
    self.assertEqual(tags.count(), 2)
    self.assertIn(tag1, tags)
    self.assertIn(tag2, tags)
  
  
  def test_create_recipe_with_ingredient(self):
    """ Test creating recipe with ingredients """
    ingredient1 = sample_ingredients(user=self.user, name='Praws')
    ingredient2 = sample_ingredients(user=self.user, name='Ginger')
    
    payload = {
      'title' : 'Chocolates Cheesecake',
      'ingredients' : [ingredient1.id, ingredient2.id],
      'time_minutes' : 30,
      'price' : 6.00
    }
    
    res = self.client.post(RECIPE_URL, payload)
    
    
    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    recipe = Recipe.objects.get(id=res.data['id'])
    ingredients = recipe.ingredients.all()
    self.assertEqual(ingredients.count(), 2)
    self.assertIn(ingredient1, ingredients)
    self.assertIn(ingredient2, ingredients)
  
  
  def test_partial_update_recipe(self):
    """ Test updating a recipe with patch """
    recipe = sample_recipe(user=self.user)
    recipe.tags.add(sample_tag(user=self.user))
    recipe.ingredients.add(sample_ingredients(user=self.user))
    
    new_tag = sample_tag(user=self.user, name='Curry')
    
    payload = { 'title' : 'Chicken Tikka', 'tags' : [new_tag.id]}
    
    url = detail_url(recipe.id)
    self.client.patch(url, payload)
    
    recipe.refresh_from_db()
    
    self.assertEqual(recipe.title, payload['title'])
    tags = recipe.tags.all()
    self.assertEqual(len(tags), 1)
    self.assertIn(new_tag, tags)
  
  
  def test_full_update_recipe(self):
    """ Test updating a recipe with put """
    recipe = sample_recipe(user=self.user)
    recipe.tags.add(sample_tag(user=self.user))
    recipe.ingredients.add(sample_ingredients(user=self.user))
    
    payload = {
			'title': 'Spaghetti carbonara',
			'time_minutes': 25,
			'price': 5.00
		}
    
    url = detail_url(recipe.id)
    self.client.put(url, payload)
    
    recipe.refresh_from_db()
    
    self.assertEqual(recipe.title, payload['title'])
    self.assertEqual(recipe.time_minutes, payload['time_minutes'])
    self.assertEqual(recipe.price, payload['price'])
    tags = recipe.tags.all()
    self.assertEqual(len(tags), 0)
    ingredients = recipe.ingredients.all()
    self.assertEqual(len(ingredients), 0)
