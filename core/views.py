from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import UserRegisterForm, UserProfileForm
from datetime import date

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Tài khoản {username} đã được tạo thành công! Bạn có thể đăng nhập ngay bây giờ.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hồ sơ của bạn đã được cập nhật thành công!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    
    context = {
        'form': form,
        'profile': request.user.userprofile
    }
    return render(request, 'profile.html', context)

@login_required
def search_users(request):
    # Lấy tiêu chuẩn ghép đôi của người dùng hiện tại
    user_profile = request.user.userprofile
    
    # Lấy tất cả người dùng trừ người dùng hiện tại
    users = User.objects.exclude(id=request.user.id)
    
    # Áp dụng các bộ lọc
    if user_profile.preferred_gender:
        users = users.filter(userprofile__gender=user_profile.preferred_gender)
    
    if user_profile.min_age:
        min_birth_date = date.today().replace(year=date.today().year - user_profile.min_age)
        users = users.filter(userprofile__birth_date__lte=min_birth_date)
    
    if user_profile.max_age:
        max_birth_date = date.today().replace(year=date.today().year - user_profile.max_age - 1)
        users = users.filter(userprofile__birth_date__gt=max_birth_date)
    
    if user_profile.preferred_location:
        users = users.filter(userprofile__location__icontains=user_profile.preferred_location)
    
    # Tìm kiếm theo tên người dùng hoặc địa điểm
    search_query = request.GET.get('q', '')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(userprofile__location__icontains=search_query)
        )
    
    context = {
        'users': users,
        'search_query': search_query,
        'user_profile': user_profile
    }
    return render(request, 'search.html', context)
