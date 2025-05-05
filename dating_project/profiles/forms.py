from django import forms
from .models import Profile, ProfileImage

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'interests', 'height', 'profession', 'education')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'interests': forms.Textarea(attrs={'rows': 3}),
        }

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = ('image', 'is_primary')
