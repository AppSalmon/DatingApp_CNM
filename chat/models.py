from django.db import models
from django.contrib.auth.models import User


class Conversations(models.Model):
    participants = models.ManyToManyField(
        User,
        related_name="conversations",  # Đổi related_name để rõ ràng hơn
        blank=False  # Đảm bảo không để trống
    )

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"

    def __str__(self):
        return f"Conversation {self.id} - Participants: {', '.join(user.username for user in self.participants.all())}"


class Messages(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages",  # Đổi related_name để rõ ràng hơn
        blank=False
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages",  # Đổi related_name để rõ ràng hơn
        blank=False
    )
    conversation = models.ForeignKey(
        Conversations,
        on_delete=models.CASCADE,
        related_name="messages",  # Đổi related_name để rõ ràng hơn
        blank=False
    )
    message_content = models.TextField(
        max_length=500,
        blank=False
    )
    created_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['created_on']  # Sắp xếp theo thời gian tạo

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.created_on}"


# class Winks(models.Model):
#     sender = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="sent_winks",  # Đổi related_name
#         blank=False
#     )
#     receiver = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="received_winks",  # Đổi related_name
#         blank=False
#     )

# class Winks(models.Model):
#     sender = models.ForeignKey(
#         User, related_name='winks_sender', on_delete=models.CASCADE)
#     receiver = models.OneToOneField(
#         User, related_name='winks_receiver', on_delete=models.CASCADE)

#     created_on = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     class Meta:
#         verbose_name = "Wink"
#         verbose_name_plural = "Winks"
#         ordering = ['created_on']

#     def __str__(self):
#         return f"Wink from {self.sender.username} to {self.receiver.username} at {self.created_on}"


class Winks(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_winks",
        blank=False
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_winks",  # Sửa từ winks_receiver thành received_winks
        blank=False
    )
    created_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Wink"
        verbose_name_plural = "Winks"
        ordering = ['created_on']
        unique_together = ('sender', 'receiver')  # Đảm bảo mỗi cặp sender-receiver chỉ có một wink

    def __str__(self):
        return f"Wink from {self.sender.username} to {self.receiver.username} at {self.created_on}"


class Views(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_views",  # Đổi related_name
        blank=False
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_views",  # Đổi related_name
        blank=False
    )
    created_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "View"
        verbose_name_plural = "Views"
        ordering = ['created_on']

    def __str__(self):
        return f"View from {self.sender.username} to {self.receiver.username} at {self.created_on}"


class Reject(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_rejects",  # Đổi related_name
        blank=False
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_rejects",  # Đổi related_name
        blank=False
    )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reject"
        verbose_name_plural = "Rejects"
        ordering = ['created_on']

    def __str__(self):
        return f"Reject from {self.sender.username} to {self.receiver.username} at {self.created_on}"
