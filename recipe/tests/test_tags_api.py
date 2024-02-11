from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer 


TAG_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
  """ Test the public available api """
  
  def setUp(self):
    self.client = APIClient()
  
  
  def test_login_required(self):
    """ test that login is required for retriving tags """
    
    res = self.client.get(TAG_URL)
    
    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
  """ Test the api for authenticated user """
  
  def setUp(self):
    self.user = get_user_model().objects.create_user(
      email = 'test@example.com',
      password = 'test1234'
    )
    
    self.client = APIClient()
    self.client.force_authenticate(self.user)
  
  
  def test_retrieve_tags(self):
    """test retrieveing tags"""
    Tag.objects.create(user=self.user, name='Vegan')
    Tag.objects.create(user=self.user, name='Fruits')
    
    res = self.client.get(TAG_URL)
    
    tags = Tag.objects.all().order_by('-name')
    serializer = TagSerializer(tags, many=True)
    
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)
  
  def Test_tags_limited_to_user(self):
    """ Test that tags limited to the authenticated user only """
    user2 = get_user_model().objects.create_user(
      "other@example.com",
      'testpass'
    )
    
    Tag.objects.create(user=user2, name='Dessert')
    tag = Tag.objects.create(user=self.user, name='Vegan')
    
    res = self.client.get(TAG_URL)
    
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(len(res.data), 1)
    self.assertEqual(res.data[0]['name'], tag.name )