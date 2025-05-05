from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Nhập tin nhắn của bạn...'
        })
    )

    class Meta:
        model = Message
        fields = ['content'] 