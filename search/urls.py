from django.urls import path, include
from search.views import search

urlpatterns = [
    path('', search, name="search"),
]
