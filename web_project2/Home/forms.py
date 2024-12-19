from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import InfoUser

class EditUserProfile(UserChangeForm):
    class Meta: 
        model = User
        fields = ('first_name', 'last_name', 'email')

class EditUserInfo(UserChangeForm):
    class Meta:
        model = InfoUser
        fields = ('birth_date', 'gender', 'country')