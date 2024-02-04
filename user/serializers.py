from django.contrib.auth import get_user_model , authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
  """Serializer for user object"""
  class Meta:
    model = get_user_model()
    fields = ('email', 'password', 'name')
    extra_kwargs = {'password': {'write_only' : True, 'min_length': 5}}
  
  
  def create(self, validated_data):
    """ Create a new user with encripted password and return it """
    return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
  """Serializer for create auth token"""
  email = serializers.CharField(label=_("email"))
  password = serializers.CharField(
    label=_("Password"),
    style={'input_type':'password'},
    trim_whitespace=False
  )
  
  def validate(self, attrs):
    email = attrs.get('email')
    password = attrs.get('password')
    
    if email and password:
      user = authenticate(request=self.context.get('request'), username=email, password=password)
      
      if not user:
        msg = _('Unable to log in with provided credentials.')
        raise serializers.ValidationError(msg, code='authorization')
    else:
      msg =_('Must enter email and password')
      raise serializers.ValidationError(msg, code='authorization')
    
    attrs['user'] = user
    return attrs