from django.urls import path,include
from . import views as v
urlpatterns=[
    path('',v.signup,name='signup'),
    path('home/',v.home,name='home'),
    path('createpost/',v.createpost,name='createpost'),
    path('updatepost/<int:pk>/',v.updatepost,name='updatepost'),
    path('forbidden/',v.forbidden,name='forbidden'),
]