# from django.shortcuts import render
# from profiles.models import Profile, ProfileImage
# from django.db.models import Q, F
# from django.db.models import Count
# from django.contrib.auth.decorators import login_required
# import datetime as DT
# from django.contrib.auth.models import User
# from chat.models import Conversations
# import datetime
# import stripe
# from checkout.models import Subscription

# # Home page after user logs in
# @login_required
# def index(request):

    
#     # Query profiles in distance order for 'Closest to you' section
#     if request.user.profile.looking_for == "BOTH":
#         closest_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).exclude(user_id=request.user.id).all()[:4]
#     else:
#         closest_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).exclude(user_id=request.user.id).all()[:4]
    
#     # Profiles for quick match finder, exclude users winked or rejected previously
#     if request.user.profile.looking_for == "BOTH":
#         card_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).exclude(user__winks_receiver__sender_id=request.user.id).exclude(user_id=request.user.id).exclude(user__rejected_receiver__sender_id=request.user.id).all()[:10]
#     else:
#         card_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).exclude(user__winks_receiver__sender_id=request.user.id).exclude(user_id=request.user.id).exclude(user__rejected_receiver__sender_id=request.user.id).all()[:10]
    
#     if card_profiles.count() == 0:
#         card_profiles_exists = False
#     else: 
#         card_profiles_exists = True
    
    
#     today = DT.date.today()
#     one_week_ago = today - DT.timedelta(days=7)
#     # Profiles for active most recently, excluding those who signed up in the last 7 days
#     if request.user.profile.looking_for == "BOTH":
#         active_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(user__date_joined__lte=one_week_ago).order_by('-user__last_login').exclude(user_id=request.user.id).all()[:4]
#     else:
#         active_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).filter(user__date_joined__lte=one_week_ago).order_by('-user__last_login').exclude(user_id=request.user.id).all()[:4] 
    
#     # Profiles ordered by signed up date for 'Newcomers' section
#     if request.user.profile.looking_for == "BOTH":
#         newest_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).order_by('-user__date_joined').exclude(user_id=request.user.id).all()[:4]
#     else:
#         newest_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).order_by('-user__date_joined').exclude(user_id=request.user.id).all()[:4] 

#     context = {
#         'page_ref': 'home',
#         'card_profiles_exists' : card_profiles_exists,
#         'closest_profiles':closest_profiles,
#         'active_profiles':active_profiles,
#         'newest_profiles': newest_profiles,
#         'card_profiles': card_profiles
#     }
    
#     return render(request, 'home.html', context)
    
# # Home page before logged in/registered
# def preregister(request):
        
#     return render(request, 'index.html')



# from django.shortcuts import render
# from profiles.models import Profile, ProfileImage
# from django.db.models import Q, F
# from django.db.models import Count
# from django.contrib.auth.decorators import login_required
# import datetime as DT
# from django.contrib.auth.models import User
# from chat.models import Conversations
# import datetime
# import stripe
# from checkout.models import Subscription

# # Home page after user logs in
# @login_required
# def index(request):

    
#     # Query profiles in distance order for 'Closest to you' section
#     if request.user.profile.looking_for == "BOTH":
#         closest_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).exclude(user_id=request.user.id).all()[:4]
#     else:
#         closest_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).exclude(user_id=request.user.id).all()[:4]
    
#     # Profiles for quick match finder, exclude users winked or rejected previously
#     if request.user.profile.looking_for == "BOTH":
#         card_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).exclude(user__winks_receiver__sender_id=request.user.id).exclude(user_id=request.user.id).exclude(user__rejected_receiver__sender_id=request.user.id).all()[:10]
#     else:
#         card_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).order_by('distance').filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).exclude(user__winks_receiver__sender_id=request.user.id).exclude(user_id=request.user.id).exclude(user__rejected_receiver__sender_id=request.user.id).all()[:10]
    
#     if card_profiles.count() == 0:
#         card_profiles_exists = False
#     else: 
#         card_profiles_exists = True
    
    
#     today = DT.date.today()
#     one_week_ago = today - DT.timedelta(days=7)
#     # Profiles for active most recently, excluding those who signed up in the last 7 days
#     if request.user.profile.looking_for == "BOTH":
#         active_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(user__date_joined__lte=one_week_ago).order_by('-user__last_login').exclude(user_id=request.user.id).all()[:4]
#     else:
#         active_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).filter(user__date_joined__lte=one_week_ago).order_by('-user__last_login').exclude(user_id=request.user.id).all()[:4] 
    
#     # Profiles ordered by signed up date for 'Newcomers' section
#     if request.user.profile.looking_for == "BOTH":
#         newest_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).order_by('-user__date_joined').exclude(user_id=request.user.id).all()[:4]
#     else:
#         newest_profiles = Profile.objects.nearby_locations(float(request.user.profile.citylat), float(request.user.profile.citylong)).filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).order_by('-user__date_joined').exclude(user_id=request.user.id).all()[:4] 

#     context = {
#         'page_ref': 'home',
#         'card_profiles_exists' : card_profiles_exists,
#         'closest_profiles':closest_profiles,
#         'active_profiles':active_profiles,
#         'newest_profiles': newest_profiles,
#         'card_profiles': card_profiles
#     }
    
#     return render(request, 'home.html', context)
    
# # Home page before logged in/registered
# def preregister(request):
        
#     return render(request, 'index.html')


from django.shortcuts import render
from profiles.models import Profile, ProfileImage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import datetime as DT

@login_required
def index(request):
    """
    Hiển thị trang chủ với danh sách hồ sơ phù hợp.
    
    Parameters:
        request: HttpRequest object
    
    Returns:
        Render template home.html với context chứa các danh sách hồ sơ và ảnh
    """
    # Kiểm tra hồ sơ và tọa độ
    if not hasattr(request.user, 'profile') or not request.user.profile.citylat or not request.user.profile.citylong:
        return render(request, 'home.html', {'error': 'Thông tin hồ sơ hoặc vị trí không hợp lệ'})

    try:
        lat = float(request.user.profile.citylat)
        long = float(request.user.profile.citylong)
    except (ValueError, TypeError):
        return render(request, 'home.html', {'error': 'Tọa độ không hợp lệ'})

    # Cơ sở truy vấn chung với prefetch ảnh
    base_query = (Profile.objects
                  .nearby_locations(lat, long)
                  .select_related('user')
                  .prefetch_related('user__profile_images')  # Tối ưu truy vấn ảnh
                  .filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH"))
                  .exclude(user_id=request.user.id))

    # Thêm điều kiện giới tính
    if request.user.profile.looking_for != "BOTH":
        base_query = base_query.filter(gender=request.user.profile.looking_for)

    # Closest to you
    closest_profiles = base_query.order_by('distance')[:4]

    # Quick match finder
    card_profiles = (base_query
                     .exclude(user__received_winks__sender=request.user)
                     .exclude(user__received_rejects__sender=request.user)
                     .order_by('distance')[:10])

    card_profiles_exists = card_profiles.exists()

    today = DT.date.today()
    one_week_ago = today - DT.timedelta(days=7)

    # Active most recently
    active_profiles = (base_query
                       .filter(user__date_joined__lte=one_week_ago)
                       .order_by('-user__last_login')[:4])

    # Newcomers
    newest_profiles = base_query.order_by('-user__date_joined')[:4]

    # Hàm để lấy ảnh APPROVED đầu tiên
    def get_profile_image(profile):
        image = profile.user.profile_images.filter(is_verified='APPROVED').first()
        return image.image.url if image else '/media/avatars/default_avt.png'

    # Tạo danh sách profile với ảnh
    closest_profiles_with_images = [(profile, get_profile_image(profile)) for profile in closest_profiles]
    card_profiles_with_images = [(profile, get_profile_image(profile)) for profile in card_profiles]
    active_profiles_with_images = [(profile, get_profile_image(profile)) for profile in active_profiles]
    newest_profiles_with_images = [(profile, get_profile_image(profile)) for profile in newest_profiles]

    # Debug
    for profile_set, name in [
        (closest_profiles, "Closest"),
        (card_profiles, "Card"),
        (active_profiles, "Active"),
        (newest_profiles, "Newest")
    ]:
        print(f"{name} profiles:", [(p.user.id, p.user.username) for p in profile_set])
        for profile in profile_set:
            images = profile.user.profile_images.filter(is_verified='APPROVED')
            print(f"Images for {profile.user.username}: {[img.image.url for img in images]}")

    context = {
        'page_ref': 'home',
        'card_profiles_exists': card_profiles_exists,
        'closest_profiles': closest_profiles_with_images,
        'card_profiles': card_profiles_with_images,
        'active_profiles': active_profiles_with_images,
        'newest_profiles': newest_profiles_with_images
    }
    return render(request, 'home.html', context)

def preregister(request):
    """
    Hiển thị trang chủ trước khi đăng nhập/đăng ký.
    
    Parameters:
        request: HttpRequest object
    
    Returns:
        Render template index.html
    """
    return render(request, 'index.html')