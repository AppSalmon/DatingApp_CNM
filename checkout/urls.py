from django.urls import path
from .views import subscribe, bank_info

urlpatterns = [
    path('', subscribe, name='subscribe'),
    path('bank-info/', bank_info, name='bank_info'),
]