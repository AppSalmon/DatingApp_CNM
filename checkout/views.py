from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from .forms import OrderForm
from .models import Subscription, Order  # Sửa đổi: Thêm import Order
from profiles.models import Profile


# Hàm cập nhật trạng thái premium cho người dùng
def make_user_premium(request):
    profile = Profile.objects.get(user_id=request.user.id)
    profile.is_premium = True
    profile.save()
    return


# Trang đăng ký, hiển thị form chọn gói và thông tin đơn hàng
@login_required
def subscribe(request):
    plan_ids = {
        'plan_F5eyNlWXHig7YB': '6 Monthly',
        'plan_F5ey2nnZwy5v8Q': '3 Monthly',
        'plan_F5eyGdYCvZPtON': 'Monthly'
    }
    
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()
            
            # Lưu tạm order_id vào session để sử dụng ở bước xác nhận
            request.session['order_id'] = order.id
            
            # Chuyển hướng đến trang hiển thị thông tin ngân hàng
            return redirect(reverse('bank_info'))
        else:
            messages.error(request, "Thông tin đơn hàng không hợp lệ")
    else:
        order_form = OrderForm()
      
    return render(request, 'subscribe.html', {'page_ref': 'subscribe', 'order_form': order_form})


# Trang hiển thị thông tin ngân hàng và nút xác nhận
@login_required
def bank_info(request):
    if request.method == 'POST':
        order_id = request.session.get('order_id')
        if not order_id:
            messages.error(request, "Không tìm thấy đơn hàng")
            return redirect(reverse('subscribe'))
        
        # Lưu subscription và cập nhật trạng thái premium
        order = Order.objects.get(id=order_id)
        plan_ids = {
            'plan_F5eyNlWXHig7YB': '6 Monthly',
            'plan_F5ey2nnZwy5v8Q': '3 Monthly',
            'plan_F5eyGdYCvZPtON': 'Monthly'
        }
        subscription = Subscription(
            user=request.user,
            plan=plan_ids[order.plans],
            customer_id=f"manual_{order.id}"  # Sử dụng ID tạm để thay thế Stripe
        )
        subscription.save()
        make_user_premium(request)
        messages.success(request, "Thanh toán thành công! Bạn giờ là người dùng premium.")
        
        # Xóa order_id khỏi session
        del request.session['order_id']
        
        return redirect(reverse('index'))
    
    # Thông tin ngân hàng
    bank_info = {
        'account_number': '5677799979',
        'bank_name': 'MB Bank'
    }
    return render(request, 'bank_info.html', {'bank_info': bank_info})