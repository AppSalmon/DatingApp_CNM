from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('O', 'Khác'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, verbose_name="Giới thiệu bản thân")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Ngày sinh")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name="Giới tính")
    location = models.CharField(max_length=100, blank=True, verbose_name="Địa điểm")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Ảnh đại diện")
    
    # Tiêu chuẩn ghép đôi
    preferred_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name="Giới tính mong muốn")
    min_age = models.IntegerField(null=True, blank=True, verbose_name="Độ tuổi tối thiểu")
    max_age = models.IntegerField(null=True, blank=True, verbose_name="Độ tuổi tối đa")
    preferred_location = models.CharField(max_length=100, blank=True, verbose_name="Địa điểm mong muốn")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
