"""
dating_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

# Import URL patterns từ các ứng dụng
from profiles import urls as profile_urls
from chat import urls as chat_urls
from home import urls as home_urls
from account import urls as account_urls
from checkout import urls as subscribe_urls
from search import urls as search_urls

# Định nghĩa URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(home_urls)),  # Trang chủ
    path('profiles/', include(profile_urls)),  # Profile URLs
    path('chat/', include(chat_urls)),  # Chat URLs
    path('subscribe/', include(subscribe_urls)),  # Checkout/Subscribe URLs
    path('my-account/', include(account_urls)),  # Account URLs
    path('search/', include(search_urls)),  # Search URLs
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # Phục vụ file media
]

# Thêm static và media URLs trong môi trường DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)