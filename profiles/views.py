from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.forms import modelformset_factory
from profiles.forms import UserLoginForm, UserRegistrationForm, ProfileForm, ProfileImageForm, MessagesForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Profile, ProfileImage
from chat.models import Conversations, Messages, Views
from checkout.models import Subscription

"""
Hàm kiểm tra xem hồ sơ thành viên có khớp với sở thích giới tính của người dùng hiện tại hay không.
Ngăn người dùng truy cập hồ sơ không phù hợp với sở thích của họ.
"""
def looking_for_check(request, user_one, user_two):
    if not user_one == user_two:
        if user_one.looking_for == "MALE":
            if not user_two.gender == "MALE":
                return redirect(reverse('index'))
        elif user_one.looking_for == "FEMALE":
            if not user_two.gender == "FEMALE":
                return redirect(reverse('index'))

# Hàm trả về chiều cao theo định dạng feet và inches từ giá trị lựa chọn
def height_choices(member_height):
    height = {
        "152.40": "5' 0",
        "154.94":"5' 1",
        "157.48":"5' 2",
        "160.02":"5' 3",
        "162.56":"5' 4",
        "165.10":"5' 5",
        "167.64":"5' 6",
        "170.18":"5' 7",
        "172.72":"5' 8",
        "175.26":"5' 9",
        "177.80":"5' 10",
        "180.34":"5' 11",
        "182.88":"6' 0",
        "185.42":"6' 1",
        "187.96":"6' 2",
        "190.50":"6' 3",
        "193.04":"6' 4",
        "195.58":"6' 5",
        "198.12":"6' 6",
        "200.66":"6' 7",
        "203.20":"6' 8",
        "205.74":"6' 9",
        "208.28":"6' 10",
        "210.82":"6' 11"
    }
    return height[member_height]

# URL để đăng xuất người dùng
@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "Bạn đã đăng xuất thành công")
    return redirect(reverse('preregister'))

# URL để xóa tài khoản người dùng
@login_required
def delete(request):
    try:
        user = User.objects.get(pk=request.user.id)
        user.delete()
        messages.success(request, "Tài khoản của bạn đã được xóa") 
    except:
        messages.success(request, "Có lỗi xảy ra. Vui lòng liên hệ chúng tôi để biết thêm chi tiết") 
    return redirect(reverse('preregister'))

# Trang đăng nhập
def login(request):
    # Nếu người dùng đã đăng nhập, chuyển hướng về trang chủ
    if request.user.is_authenticated:
        return redirect(reverse('index'))
        
    # Nếu người dùng gửi form đăng nhập
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            if user:
                messages.success(request, "Đăng nhập thành công")
                auth.login(user=user, request=request)
                return redirect(reverse('index'))
            else: 
                messages.error(request, "Tên người dùng hoặc mật khẩu không đúng")
    else:
        login_form = UserLoginForm()
            
    context = {
        'login_form': login_form
    }
    return render(request, 'login.html', context)
    
# Trang đăng ký tài khoản
def register(request):
    # Nếu người dùng gửi form đăng ký
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
            if user:
                messages.success(request, "Tài khoản của bạn đã được tạo")
                auth.login(user=user, request=request)
                return redirect(reverse('create_profile'))
            else:
                messages.error(request, "Không thể tạo tài khoản của bạn")
    else:
        registration_form = UserRegistrationForm()
        
    context = {
        'registration_form': registration_form
    }
    return render(request, 'register.html', context)

# Trang tạo/chỉnh sửa hồ sơ người dùng
@login_required  
def create_profile(request):
    """
    Tạo formset để cho phép tải lên nhiều ảnh hồ sơ.
    """
    ImageFormSet = modelformset_factory(ProfileImage, form=ProfileImageForm, extra=6, max_num=6, help_texts=None)
    
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        image_form = ProfileImageForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ProfileImage.objects.filter(user_id=request.user.id).all())
        
        # Cập nhật hồ sơ và đặt trạng thái là 'chờ phê duyệt'
        if profile_form.is_valid() and formset.is_valid():
            instance = profile_form.save(commit=False)
            instance.user_id = request.user.id
            instance.is_verified = 'TO BE APPROVED'
            instance.save()
            
            # Xóa các ảnh được yêu cầu xóa
            deleted_images = request.POST.getlist('delete')
            for image in deleted_images:
                if not image == "None":
                    ProfileImage.objects.get(pk=image).delete()
                    
            # Lưu các ảnh được gửi lên
            for form in formset:
                if form.is_valid() and form.has_changed():
                    instance_image = form.save(commit=False)
                    instance_image.user = request.user
                    instance_image.is_verified = False
                    instance_image.save()

            return redirect(reverse('verification_message'))
            
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        image_form = ProfileImageForm(instance=request.user.profile)
        initial_images = [{'image_url': i.image} for i in ProfileImage.objects.filter(user_id=request.user.id).all() if i.image]
        formset = ImageFormSet(queryset=ProfileImage.objects.filter(user_id=request.user.id).all(), initial=initial_images)
        
    context = {
        'page_ref': 'create_profile',
        'profile_form': profile_form,
        'image_form': image_form,
        'formset': formset
    }
    return render(request, 'create-profile.html', context)    

# Trang xem hồ sơ của một thành viên
@login_required 
def member_profile(request, id):
    """
    Hiển thị hồ sơ của một thành viên và cho phép gửi tin nhắn (yêu cầu premium).
    
    Parameters:
        request: HttpRequest object
        id: ID của người dùng cần xem hồ sơ
    
    Returns:
        Render template member.html với dữ liệu hồ sơ và form tin nhắn
    """
    # Lấy thông tin thành viên
    # member = User.objects.get(id=id)
    try:
        member = User.objects.get(id=id)
        print(f"Member: {member.username}, ID: {id}")  # Debug
        images = member.profile_images.all()
        print(f"Images for {member.username}: {[(img.image.url, img.is_verified) for img in images]}")  # Debug


    except User.DoesNotExist:
        messages.error(request, "Người dùng không tồn tại")
        return redirect(reverse('index'))
    
    height = height_choices(str(member.profile.height))
    
    # Kiểm tra xem thành viên có phải là người dùng hiện tại không
    if not member == request.user:
        current_user = False
        
        # Kiểm tra sở thích giới tính
        result = looking_for_check(request, request.user.profile, member.profile)
        if result:
            return result
        result = looking_for_check(request, member.profile, request.user.profile)
        if result:
            return result
        
        # Thêm lượt xem nếu chưa xem hoặc lượt xem trước chưa được đọc
        last_view = Views.objects.filter(receiver_id=id).filter(sender_id=request.user.id).last()
        if not last_view or last_view.is_read:
            view = Views(receiver=member, sender=request.user)
            view.save()
        
        # Xử lý gửi tin nhắn
        if request.method == "POST" and 'message_submit' in request.POST:
            message_form = MessagesForm(request.POST)
            if message_form.is_valid():
                # Sửa đổi: Chỉ kiểm tra is_premium, không dùng Stripe
                if request.user.profile.is_premium:
                    # Tạo hoặc lấy cuộc trò chuyện
                    conversation = Conversations.objects.filter(participants=request.user.id).filter(participants=id)
                    if conversation.exists():
                        message = message_form.save(commit=False)
                        message.sender = request.user
                        message.receiver = User.objects.get(pk=id)
                        message.conversation = conversation[0]
                        message.save()
                        return redirect('/chat/%s' % conversation[0].id)
                    else:
                        receiver = User.objects.get(pk=id)
                        conversation = Conversations()
                        conversation.save()
                        conversation.participants.add(request.user.id)
                        conversation.participants.add(receiver)
                        message = message_form.save(commit=False)
                        message.sender = request.user
                        message.receiver = receiver
                        message.conversation = conversation
                        message.save()
                        return redirect('/chat/%s' % conversation.id)
                else:
                    messages.error(request, "Bạn cần gói premium để gửi tin nhắn")
                    return redirect(reverse('subscribe'))
        else:
            message_form = MessagesForm()
    else:
        message_form = MessagesForm()
        current_user = True
        
    context = {
        'height': height,
        'page_ref': 'member_profile',
        'member': member,
        'message_form': message_form,
        'current_user': current_user
    }
    return render(request, 'member.html', context)
    
# Trang hiển thị thông báo xác minh
def verification_message(request):
    return render(request, 'verification-message.html')