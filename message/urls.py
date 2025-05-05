from django.urls import path
from . import views

app_name = 'message'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:conversation_id>/', views.conversation, name='conversation'),
    path('new/<int:user_id>/', views.new_conversation, name='new_conversation'),
    path('unread-count/', views.get_unread_count, name='unread_count'),
] 