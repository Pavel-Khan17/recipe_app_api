from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminTest(TestCase):
  
  def setUp(self):
    """seting up the testing enveroment for pre test process """
    self.client = Client()
    self.admin_user = get_user_model().objects.create_superuser(
      email  = 'testsuperuser@example.com',
      password = 'password1234'
    )
    self.client.force_login(self.admin_user)
    self.user = get_user_model().objects.create_user(
      email = 'test@example.com',
      password ='test1234',
      name = 'test user full name'
    )
  
  def test_user_listed(self):
    """ test that user are listed on the page """
    url = reverse('admin:core_user_changelist')
    res = self.client.get(url)
    
    
    self.assertContains(res, self.user.name)
    self.assertContains(res, self.user.email)
  
  def test_user_change_page(self):
    """ test that user are edit page works """
    url = reverse('admin:core_user_change', args=[self.user.id])
    res = self.client.get(url)
    
    self.assertEqual(res.status_code , 200)
  
  def test_user_add_page(self):
    """ test that user create page works """
    url = reverse('admin:core_user_add')
    res = self.client.get(url)
    
    self.assertEqual(res.status_code, 200)