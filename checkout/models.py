from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    PLANS = (
        ('plan_F5eyGdYCvZPtON', 'Monthly - £24.99'),
        ('plan_F5ey2nnZwy5v8Q', '3 Months - £49.99'),
        ('plan_F5eyNlWXHig7YB', '6 Months - £74.99'),
    )
    plans = models.CharField(
        max_length=100,
        choices=PLANS,
        default='plan_F5ey2nnZwy5v8Q',
        blank=False
    )
    full_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=40, blank=False)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, blank=False)
    street_address1 = models.CharField(max_length=40, blank=False)
    street_address2 = models.CharField(max_length=40, blank=True)  # Đổi blank=True vì đây là địa chỉ phụ
    county = models.CharField(max_length=40, blank=False)
    date = models.DateField(auto_now_add=True)  # Tự động thêm ngày tạo

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-date']  # Sắp xếp theo ngày, mới nhất trước

    def __str__(self):
        return f"Order {self.id} - {self.full_name} - {self.date}"


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Thêm on_delete
        related_name="subscriptions",  # Thêm related_name để truy vấn ngược
        null=False,
        blank=False
    )
    plan = models.CharField(max_length=255, blank=False)
    customer_id = models.CharField(max_length=255, blank=False)

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return f"Subscription for {self.user.username} - Plan: {self.plan}"