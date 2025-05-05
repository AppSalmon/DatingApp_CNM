from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from profiles.models import Profile

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Tạo profile cho user mới
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('profile_edit')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def account_settings(request):
    return render(request, 'accounts/settings.html')
