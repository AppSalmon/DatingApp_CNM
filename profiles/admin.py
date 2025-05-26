# profiles/admin.py
from django.contrib import admin
from .models import Profile, ProfileImage
from django.contrib import messages

def verify(modeladmin, request, queryset):
    queryset.update(is_verified='APPROVED')
    messages.success(request, "Đã xác minh thành công hồ sơ/hình ảnh đã chọn.")

def reject(modeladmin, request, queryset):
    if isinstance(queryset.first(), Profile):
        queryset.update(is_verified='NOT_APPROVED')
        messages.success(request, "Hồ sơ đã chọn được đánh dấu là không được chấp thuận.")
    else:
        queryset.delete()
        messages.success(request, "Đã xóa những hình ảnh đã chọn.")

verify.short_description = "Đánh dấu đã chọn là đã xác minh"
reject.short_description = "Đánh dấu đã chọn là bị từ chối"

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'is_verified')
    list_filter = ('is_verified', )
    readonly_fields = ('id',)
    actions = (verify, reject)
    list_per_page = 30
    
admin.site.register(Profile, ProfileAdmin)

class ProfileImageAdmin(admin.ModelAdmin):
    model = ProfileImage
    actions = (verify, reject)
    list_display = ('user', 'image', 'thumbnail', 'is_verified')

    def thumbnail(self, obj):
        return '<img src="{thumb}" width="150" />'.format(thumb=obj.image.url)
        
    thumbnail.allow_tags = True
    thumbnail.short_description = 'Image'
    
admin.site.register(ProfileImage, ProfileImageAdmin)