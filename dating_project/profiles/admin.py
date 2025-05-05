from django.contrib import admin
from .models import Profile, ProfileImage

class ProfileImageInline(admin.TabularInline):
    model = ProfileImage
    extra = 1

class ProfileAdmin(admin.ModelAdmin):
    inlines = [ProfileImageInline]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileImage)
