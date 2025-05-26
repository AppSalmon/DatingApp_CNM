from django.urls import path, re_path
from .views import account

urlpatterns = [
    path('', account, name='account'),
  
]