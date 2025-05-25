from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from checkout.models import Subscription
from django.contrib import messages
from django.contrib.auth.models import User
from profiles.models import Profile
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from profiles.forms import EditProfileForm

# Trang hiển thị và chỉnh sửa thông tin tài khoản người dùng
@login_required
def account(request):
    """
    Hiển thị thông tin tài khoản, trạng thái đăng ký, và cho phép chỉnh sửa
    email, tên người dùng, hoặc mật khẩu.
    
    Parameters:
        request: HttpRequest object
    
    Returns:
        Render template account.html với dữ liệu đăng ký, trạng thái premium,
        và các form chỉnh sửa
    """
    # Lấy thông tin đăng ký và trạng thái premium
    subscription = Subscription.objects.filter(user_id=request.user.id).first()
    profile = Profile.objects.get(user_id=request.user.id)
    is_premium = profile.is_premium
    
    # Xử lý form chỉnh sửa tài khoản
    if request.method == "POST" and 'account-change-submit' in request.POST:
        password_form = PasswordChangeForm(request.user)
        user_form = EditProfileForm(request.POST, instance=request.user, user=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Thông tin tài khoản đã được cập nhật")
        else:
            messages.error(request, "Không thể cập nhật thông tin tài khoản")
    
    # Xử lý form đổi mật khẩu
    elif request.method == "POST" and 'password-change-submit' in request.POST:
        user_form = EditProfileForm(instance=request.user, user=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, "Mật khẩu đã được thay đổi")
        else:
            messages.error(request, "Không thể thay đổi mật khẩu")
    
    else:
        user_form = EditProfileForm(instance=request.user, user=request.user)
        password_form = PasswordChangeForm(request.user)
    
    context = {
        'password_form': password_form,
        'user_form': user_form,
        'subscription': subscription,  # Có thể là None nếu chưa đăng ký
        'is_premium': is_premium
    }
    return render(request, 'account.html', context)