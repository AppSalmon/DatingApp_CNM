from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from profiles.models import Profile

def premium_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.profile.is_premium:
            return function(request, *args, **kwargs)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {'redirect': '/subscribe'}
                return JsonResponse(data)
            return redirect(reverse('subscribe'))
            
    return wrap