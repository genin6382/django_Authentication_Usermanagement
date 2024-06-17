from django.contrib import admin
from django.contrib.auth.models import User
from .models import Post
from django.contrib.admin.sites import AlreadyRegistered

# Register your models here.
try:
    admin.site.register(User)
except AlreadyRegistered:
    pass

admin.site.register(Post)
