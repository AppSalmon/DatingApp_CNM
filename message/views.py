from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from .models import Conversation, Message
from .forms import MessageForm

# Create your views here.

@login_required
def inbox(request):
    conversations = request.user.conversations.all()
    return render(request, 'message/inbox.html', {'conversations': conversations})

@login_required
def conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    messages = conversation.messages.all()
    
    # Đánh dấu tin nhắn chưa đọc là đã đọc
    unread_messages = messages.filter(is_read=False).exclude(sender=request.user)
    unread_messages.update(is_read=True)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            conversation.save()  # Cập nhật thời gian của cuộc trò chuyện
            return redirect('conversation', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    other_participant = conversation.participants.exclude(id=request.user.id).first()
    
    context = {
        'conversation': conversation,
        'messages': messages,
        'form': form,
        'other_participant': other_participant
    }
    return render(request, 'message/conversation.html', context)

@login_required
def new_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    # Kiểm tra xem cuộc trò chuyện đã tồn tại chưa
    existing_conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()
    
    if existing_conversation:
        return redirect('conversation', conversation_id=existing_conversation.id)
    
    # Tạo cuộc trò chuyện mới
    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, other_user)
    
    return redirect('conversation', conversation_id=conversation.id)

@login_required
def get_unread_count(request):
    unread_count = Message.objects.filter(
        conversation__participants=request.user,
        is_read=False
    ).exclude(sender=request.user).count()
    
    return JsonResponse({'unread_count': unread_count})
