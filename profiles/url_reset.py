from django.urls import path, re_path
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    path(
        '',
        PasswordResetView.as_view(
            success_url=reverse_lazy('password_reset_done')  # Thay post_reset_redirect bằng success_url
        ),
        name='password_reset'
    ),
    path('done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(
        r'^(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('password_reset_complete')  # Thay post_reset_redirect bằng success_url
        ),
        name='password_reset_confirm'
    ),
    path('complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]