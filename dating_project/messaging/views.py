from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Conversation, Message
from matching.models import Match

@login_required
def conversations(request):
    # Lấy tất cả các cuộc trò chuyện của người dùng
    user_matches = list(request.user.matches_as_user1.all()) + list(request.user.matches_as_user2.all())
    conversations = Conversation.objects.filter(match__in=user_matches)
    
    return render(request, 'messaging/conversations.html', {'conversations': conversations})

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    match = conversation.match
    
    # Xác nhận người dùng hiện tại là một phần của cuộc trò chuyện
    if request.user.id != match.user1.id and request.user.id != match.user2.id:
        messages.error(request, "Bạn không có quyền truy cập vào trang này.")
        return redirect('conversations')
    
    # Xác định người dùng khác trong cuộc trò chuyện
    other_user = match.user2 if match.user1.id == request.user.id else match.user1
    
    # Đánh dấu tin nhắn đã đọc
    Message.objects.filter(conversation=conversation, sender=other_user, is_read=False).update(is_read=True)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            return redirect('conversation_detail', conversation_id=conversation.id)
    
    messages_list = conversation.messages.order_by('created_at')
    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'other_user': other_user,
        'messages': messages_list
    })

@login_required
def send_message_ajax(request, conversation_id):
    if request.method == 'POST' and request.is_ajax():
        conversation = get_object_or_404(Conversation, id=conversation_id)
        match = conversation.match
        
        # Xác nhận người dùng hiện tại là một phần của cuộc trò chuyện
        if request.user.id != match.user1.id and request.user.id != match.user2.id:
            return JsonResponse({'status': 'error', 'message': 'Không có quyền truy cập'}, status=403)
        
        content = request.POST.get('content')
        if content:
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            
            return JsonResponse({
                'status': 'success',
                'message': {
                    'id': message.id,
                    'content': message.content,
                    'created_at': message.created_at.strftime('%Y-%m-%d %H:%M'),
                    'is_sender': True
                }
            })
        
        return JsonResponse({'status': 'error', 'message': 'Nội dung tin nhắn không hợp lệ'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Phương thức không được hỗ trợ'}, status=405)
