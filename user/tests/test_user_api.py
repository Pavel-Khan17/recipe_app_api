from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
  """ helper functions to create new users """
  return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
  """Test the users API (public)"""
  def setUp(self):
    self.client = APIClient()
  
  
  def test_create_valid_user_success(self):
    """ test that create valid user is success"""
    payload = {
      'email' : 'test@example.com',
      'password': 'test1234',
      'name' : 'test user full name'
    }
    
    res = self.client.post(CREATE_USER_URL, payload) 
    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    
    user = get_user_model().objects.get(**res.data)
    self.assertTrue(user.check_password(payload['password']))
    self.assertNotIn('password', res.data)
  
  
  def test_user_exist(self):
    """ test creating user that already exists fails"""
    payload = {'email': 'test@example.com', 'password': 'test1234'}
    create_user(**payload)
    
    res = self.client.post(CREATE_USER_URL,payload)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
  
  
  def test_user_valid_password(self):
    """ test creating user has valid password"""
    payload = {'email': 'test@example.com', 'password': 'psw'}
    
    res = self.client.post(CREATE_USER_URL, payload)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    user_exist = get_user_model().objects.filter(
      email = payload['email']
    ).exists()
    self.assertFalse(user_exist)
  
  
  def test_create_token_for_user(self):
    """ test that token is created for user"""
    payload = {'email': 'test@example.com', 'password': 'test1234'}
    create_user(**payload)
    
    res = self.client.post(TOKEN_URL, payload)
    
    self.assertIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
  
  
  def test_create_token_invalid_credentials(self):
    """ test that token is not created for invalid credentials """
    payload = {'email': 'test@example.com', 'password': 'test1234'}
    create_user(**payload)
    payload2 = {'email': 'test@example.com', 'password': 'wrong'}
    
    res = self.client.post(TOKEN_URL, payload2)
    
    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
  
  
  def test_create_token_for_no_user(self):
    """ test that token is not created for no user"""
    payload = {'email': 'test@example.com', 'password': 'test1234'}
    
    res = self.client.post(TOKEN_URL, payload)
    
    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
  
  
  def test_create_token_for_missing_credentials(self):
    """ test that token is not created for missing credentials """
    payload = {'email': 'test', 'password': ''}
    
    res = self.client.post(TOKEN_URL, payload)
    
    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)