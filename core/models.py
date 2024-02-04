from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
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