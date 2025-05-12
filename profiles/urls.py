from django.urls import path, re_path, include
from profiles.views import (
    logout,
    login,
    register,
    create_profile,
    member_profile,
    delete,
    verification_message,
)
from profiles import url_reset

urlpatterns = [
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('create-profile/', create_profile, name='create_profile'),
    path('delete/', delete, name='delete'),
    path('verification-message/', verification_message, name='verification_message'),
    re_path(r'^member/(?P<id>\d+)/$', member_profile, name='member_profile'),
    path('password-reset/', include(url_reset)),
]