from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.


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
