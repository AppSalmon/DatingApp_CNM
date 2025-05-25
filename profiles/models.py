from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.utils.crypto import get_random_string
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
import datetime
import os
import math
from django.db.models.expressions import RawSQL
import stripe
from django.db.backends.signals import connection_created
from django.dispatch import receiver
from chat.models import Conversations
from checkout.models import Subscription


# Chỉ cần thiết cho SQLite trong môi trường phát triển và kiểm thử
# Thêm các hàm toán học cho SQLite vì SQLite không hỗ trợ natively
if "DEVELOPMENT" in os.environ or "TESTING" in os.environ:
    @receiver(connection_created)
    def extend_sqlite(connection=None, **kwargs):
        cf = connection.connection.create_function
        cf('acos', 1, math.acos)
        cf('cos', 1, math.cos)
        cf('radians', 1, math.radians)
        cf('sin', 1, math.sin)


class LocationManager(models.Manager):
    # Assistance from https://stackoverflow.com/questions/19703975/django-sort-by-distance
    def nearby_locations(self, citylat, citylong, max_distance=None):
        """
        Trả về các đối tượng được sắp xếp theo khoảng cách đến tọa độ được chỉ định,
        với khoảng cách nhỏ hơn max_distance (tính bằng kilômét).
        """
        gcd_formula = (
            "6371 * acos(cos(radians(%s)) * "
            "cos(radians(citylat)) * "
            "cos(radians(citylong) - radians(%s)) + "
            "sin(radians(%s)) * sin(radians(citylat)))"
        )
        distance_raw_sql = RawSQL(gcd_formula, (citylat, citylong, citylat))

        if max_distance is not None:
            return self.annotate(distance=distance_raw_sql).filter(distance__lt=max_distance)
        return self.annotate(distance=distance_raw_sql)


class Profile(models.Model):
    HAIR_COLOUR = (
        ('BLACK', 'Black'),
        ('BLONDE', 'Blonde'),
        ('BROWN', 'Brown'),
        ('RED', 'Red'),
        ('GREY', 'Grey'),
        ('BALD', 'Bald'),
        ('BLUE', 'Blue'),
        ('PINK', 'Pink'),
        ('GREEN', 'Green'),
        ('PURPLE', 'Purple'),
        ('OTHER', 'Other'),
    )
    BODY_TYPE = (
        ('THIN', 'Thin'),
        ('AVERAGE', 'Average'),
        ('FIT', 'Fit'),
        ('MUSCULAR', 'Muscular'),
        ('A_LITTLE_EXTRA', 'A Little Extra'),
        ('CURVY', 'Curvy'),
    )
    LOOKING_FOR = (
        ('MALE', 'Men'),
        ('FEMALE', 'Women'),
        ('BOTH', 'Both'),
    )
    APPROVAL = (
        ('TO_BE_APPROVED', 'To be approved'),
        ('APPROVED', 'Approved'),
        ('NOT_APPROVED', 'Not approved'),
    )
    HAIR_LENGTH = (
        ('LONG', 'Long'),
        ('SHOULDER_LENGTH', 'Shoulder Length'),
        ('AVERAGE', 'Average'),
        ('SHORT', 'Short'),
        ('SHAVED', 'Shaved'),
    )
    ETHNICITY = (
        ('WHITE', 'White'),
        ('ASIAN_INDIAN', 'Asian: Indian'),
        ('ASIAN_PAKISTANI', 'Asian: Pakistani'),
        ('ASIAN_BANGLADESHI', 'Asian: Bangladeshi'),
        ('ASIAN_CHINESE', 'Asian: Chinese'),
        ('BLACK', 'Black'),
        ('MIXED', 'Mixed'),
        ('OTHER_ETHNICITY', 'Other Ethnicity'),
    )
    RELATIONSHIP_STATUS = (
        ('NEVER_MARRIED', 'Never Married'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
        ('SEPARATED', 'Separated'),
    )
    EDUCATION = (
        ('HIGH_SCHOOL', 'High School'),
        ('COLLEGE', 'College'),
        ('BACHELORS_DEGREE', 'Bachelors Degree'),
        ('MASTERS', 'Masters'),
        ('PHD_POST_DOCTORAL', 'PhD / Post Doctoral'),
    )
    GENDER = (
        ("MALE", "Male"),
        ("FEMALE", "Female"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",  # Đảm bảo related_name rõ ràng
        blank=False
    )
    bio = models.TextField(max_length=500, blank=False)
    gender = models.CharField(choices=GENDER, default="MALE", max_length=6, blank=False)
    hair_length = models.CharField(choices=HAIR_LENGTH, default="LONG", max_length=20, blank=False)
    ethnicity = models.CharField(choices=ETHNICITY, default="WHITE", max_length=20, blank=False)
    relationship_status = models.CharField(choices=RELATIONSHIP_STATUS, default="NEVER_MARRIED", max_length=20, blank=False)
    education = models.CharField(choices=EDUCATION, default="HIGH_SCHOOL", max_length=20, blank=False)
    height = models.DecimalField(
        max_digits=5,  # Giảm max_digits vì chiều cao không cần lớn
        decimal_places=2,
        default=180.34,
        validators=[
            MinValueValidator(100.00),  # Chiều cao tối thiểu 100 cm
            MaxValueValidator(250.00),  # Chiều cao tối đa 250 cm
        ]
    )
    hair_colour = models.CharField(choices=HAIR_COLOUR, default="BLACK", max_length=10, blank=False)
    body_type = models.CharField(choices=BODY_TYPE, default="AVERAGE", max_length=15, blank=False)
    looking_for = models.CharField(choices=LOOKING_FOR, default='BOTH', max_length=6, blank=False)
    children = models.BooleanField(default=False)
    location = models.CharField(max_length=100, blank=False)
    citylat = models.DecimalField(max_digits=9, decimal_places=6, default=-2.0180319)  # Sửa default thành số
    citylong = models.DecimalField(max_digits=9, decimal_places=6, default=52.5525525)  # Sửa default thành số
    birth_date = models.DateField(null=True, blank=True)  # Xóa default để tránh lỗi
    is_premium = models.BooleanField(default=False)
    is_verified = models.CharField(choices=APPROVAL, default="TO_BE_APPROVED", max_length=14, blank=False)

    objects = LocationManager()

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"Profile of {self.user.username}"

    # Assistance from https://stackoverflow.com/questions/5056327/define-and-insert-age-in-django-template
    def age(self):
        if self.birth_date:
            return int((datetime.date.today() - self.birth_date).days / 365.25)
        return None  # Trả về None nếu birth_date không có


# Assistance from https://stackoverflow.com/questions/2673647/enforce-unique-upload-file-names-using-django
def image_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('images/', filename)


class ProfileImage(models.Model):
    APPROVAL = (
        ('TO_BE_APPROVED', 'To be approved'),
        ('APPROVED', 'Approved'),
        ('NOT_APPROVED', 'Not approved'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Thêm on_delete
        related_name="profile_images",  # Thêm related_name
        blank=False
    )
    image = models.ImageField(upload_to=image_filename, blank=True, default='avatars/default_avt.png')
    is_verified = models.CharField(choices=APPROVAL, default="TO_BE_APPROVED", max_length=14, blank=False)

    class Meta:
        verbose_name = "Profile Image"
        verbose_name_plural = "Profile Images"

    def __str__(self):
        return f"Image for {self.user.username} - {self.is_verified}"


# Signal để tạo profile tự động khi user được tạo
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Signal để lưu profile khi user được lưu
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Signal để xử lý trước khi xóa user
def pre_delete_user(sender, instance, **kwargs):
    # Xóa tất cả các cuộc trò chuyện mà user tham gia
    conversations = Conversations.objects.filter(participants=instance)
    conversations.delete()

    # Hủy tất cả các subscription của user
    customer = Subscription.objects.filter(user=instance).first()
    if customer:
        try:
            stripe_customer = stripe.Customer.retrieve(customer.customer_id)
            for sub in stripe_customer.subscriptions.data:
                stripe.Subscription.modify(
                    sub.id,
                    cancel_at_period_end=True
                )
        except Exception as e:
            print(f"Pre-delete user failed: {str(e)}")


# Kết nối các signal
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
pre_delete.connect(pre_delete_user, sender=User)