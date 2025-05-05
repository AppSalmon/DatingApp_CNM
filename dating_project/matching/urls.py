from django.urls import path
from . import views

urlpatterns = [
    path('discover/', views.discover, name='discover'),
    path('like/<int:user_id>/', views.like_user, name='like_user'),
    path('matches/', views.matches, name='matches'),
    path('match/<int:match_id>/', views.match_detail, name='match_detail'),
]
