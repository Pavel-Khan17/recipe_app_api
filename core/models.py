from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from django.conf import settings
# Create your models here.



class UserManager(BaseUserManager):
  
  def create_user(self, email, password=None, **extra_fields):
    """ Create and save new user """
    if not email:
      raise ValueError('User must have a email address')
    user = self.model(email=self.normalize_email(email), **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    
    return user
  
  def create_superuser(self, email, password):
    """ Create and save a new super user """
    
    user = self.create_user(email,password)
    user.is_staff = True
    user.is_superuser = True 
    user.save(using=self._db)
    
    return user

class User(AbstractBaseUser, PermissionsMixin):
  """ Custom user model that supports using email instand of username """
  email = models.EmailField(max_length=200, unique=True)
  name  = models.CharField(max_length=50)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  
  
  objects = UserManager()
  
  USERNAME_FIELD = 'email'
  # Into the settings.py   AUTH_USER_MODEL = 'core.User'


class Tag(models.Model):
  name = models.CharField(max_length=250)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
  
  def __str__(self):
    return self.name


class Ingredient(models.Model):
  name = models.CharField(max_length=250)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.name


class Recipe(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  title = models.CharField(max_length=255)
  time_minutes = models.IntegerField()
  price = models.DecimalField(max_digits=5, decimal_places=2)
  link = models.CharField(max_length=255, blank=True)
  tags = models.ManyToManyField('Tag')
  ingredients = models.ManyToManyField('Ingredient')
  
  def __str__(self):
    return self.title