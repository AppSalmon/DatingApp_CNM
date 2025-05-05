from django.urls import path
from . import views

urlpatterns = [
    path('', views.conversations, name='conversations'),
    path('<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('<int:conversation_id>/send/', views.send_message_ajax, name='send_message_ajax'),
]
