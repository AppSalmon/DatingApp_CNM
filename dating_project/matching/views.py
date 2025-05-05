from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Like, Match
from accounts.models import User
from profiles.models import Profile
from messaging.models import Conversation

@login_required
def discover(request):
    # Lấy danh sách người dùng bạn chưa thích hoặc match
    liked_users = request.user.likes_given.values_list('liked_user', flat=True)
    matched_users_1 = request.user.matches_as_user1.values_list('user2', flat=True)
    matched_users_2 = request.user.matches_as_user2.values_list('user1', flat=True)
    
    # Lọc người dùng theo giới tính quan tâm (giả sử giới tính đối lập)
    if request.user.gender == 'M':
        gender_filter = 'F'
    elif request.user.gender == 'F':
        gender_filter = 'M'
    else:
        gender_filter = None
    
    potential_matches = User.objects.filter(gender=gender_filter) if gender_filter else User.objects.all()
    potential_matches = potential_matches.exclude(
        Q(id=request.user.id) | 
        Q(id__in=liked_users) | 
        Q(id__in=matched_users_1) | 
        Q(id__in=matched_users_2)
    )
    
    return render(request, 'matching/discover.html', {'potential_matches': potential_matches})

@login_required
def like_user(request, user_id):
    liked_user = get_object_or_404(User, id=user_id)
    
    # Kiểm tra xem người dùng đã thích mình chưa
    if Like.objects.filter(user=liked_user, liked_user=request.user).exists():
        # Tạo một match mới
        user1, user2 = sorted([request.user.id, liked_user.id])
        match, created = Match.objects.get_or_create(
            user1_id=user1,
            user2_id=user2
        )
        
        # Tạo cuộc trò chuyện cho match
        if created:
            Conversation.objects.create(match=match)
            messages.success(request, f'Bạn đã match với {liked_user.username}!')
        
        return redirect('match_detail', match_id=match.id)
    
    # Nếu chưa có match, tạo like mới
    Like.objects.create(user=request.user, liked_user=liked_user)
    messages.success(request, f'Bạn đã thích {liked_user.username}!')
    
    return redirect('discover')

@login_required
def matches(request):
    user_matches = list(request.user.matches_as_user1.all()) + list(request.user.matches_as_user2.all())
    return render(request, 'matching/matches.html', {'matches': user_matches})

@login_required
def match_detail(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    
    # Xác nhận người dùng hiện tại là một phần của match
    if request.user.id != match.user1.id and request.user.id != match.user2.id:
        messages.error(request, "Bạn không có quyền truy cập vào trang này.")
        return redirect('matches')
    
    # Xác định người dùng khác trong match
    other_user = match.user2 if match.user1.id == request.user.id else match.user1
    
    return render(request, 'matching/match_detail.html', {
        'match': match,
        'other_user': other_user
    })
