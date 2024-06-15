from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from django import forms
class SignupForm(UserCreationForm):
    password1=forms.CharField(help_text='')
    password2=forms.CharField(help_text='')
    username=forms.CharField(help_text='')
    class Meta:
        model=User
        fields=['first_name','last_name','username','password1','password2']
        


class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','description']
