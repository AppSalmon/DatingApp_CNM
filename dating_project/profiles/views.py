from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, ProfileImage
from .forms import ProfileForm, ProfileImageForm
from django.conf import settings

@login_required
def profile_detail(request, username):
    user = get_object_or_404(settings.AUTH_USER_MODEL, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'profiles/detail.html', {'profile': profile})

@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thông tin hồ sơ đã được cập nhật.')
            return redirect('profile_detail', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'profiles/edit.html', {'form': form})

@login_required
def profile_image_add(request):
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.profile = request.user.profile
            image.save()
            messages.success(request, 'Ảnh đã được tải lên.')
            return redirect('profile_images')
    else:
        form = ProfileImageForm()
    
    return render(request, 'profiles/image_add.html', {'form': form})

@login_required
def profile_images(request):
    profile = request.user.profile
    images = profile.images.all()
    return render(request, 'profiles/images.html', {'images': images})
