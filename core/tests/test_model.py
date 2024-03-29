from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models
# Create your tests here.


def sample_user(email='test@example.com', password='test1234'):
  """ Creating sample user """
  return get_user_model().objects.create_user(email, password)

class ModelTest(TestCase):
  
  
  def test_create_user_with_email_successful(self):
    """test creating a new user with email is successful"""
    
    email = 'test@example.com'
    password = 'test1234'
    user = get_user_model().objects.create_user(
      email = email,
      password = password
    )
    
    self.assertEqual(user.email , email)
    self.assertTrue(user.check_password(password))
  
  def test_new_user_email_normalized(self):
    """ test for a new user email is normalized"""
    
    email = 'test@EXAMPLE.COM'
    user = get_user_model().objects.create_user(email, 'test1234')
    
    self.assertEqual(user.email, email.lower())
  
  def test_new_user_invalid_email(self):
    """ test for a new user with no email rises error"""
    
    with self.assertRaises(ValueError):
      get_user_model().objects.create_user(None, 'test123')
  
  def test_create_new_super_user(self):
    """ test for create new super user """
    
    user = get_user_model().objects.create_superuser(
      'test@example.com',
      'test1234'
    )
    
    self.assertTrue(user.is_superuser)
    self.assertTrue(user.is_staff)
  
  
  def test_tag_str(self):
    """ test tag string representaion """
    
    tag = models.Tag.objects.create(
      user = sample_user(),
      name = 'vegan'
    )
    
    self.assertEqual(str(tag), tag.name)
  
  
  def test_ingredient_str(self):
    """ test recipe ingredient string representation """
    ingredient = models.Ingredient.objects.create(
      user = sample_user(),
      name = 'cucumber'
    )
    
    self.assertEqual(str(ingredient), ingredient.name)
  
  
  def test_recipe_str(self):
    """ test recipe string representation """
    recipe = models.Recipe.objects.create(
      user = sample_user(),
      title = 'Biriyani',
      time_minutes = 5,
      price = 120.00
    )
    
    self.assertEqual(str(recipe), recipe.title)