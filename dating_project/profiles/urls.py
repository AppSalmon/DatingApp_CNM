from django.urls import path
from . import views

urlpatterns = [
    path('edit/', views.profile_edit, name='profile_edit'),
    path('images/', views.profile_images, name='profile_images'),
    path('images/add/', views.profile_image_add, name='profile_image_add'),
    path('<str:username>/', views.profile_detail, name='profile_detail'),
]
