from django.db import models
from django.conf import settings
from django.db import models

# Create your models here.
class Notification(models.Model):

    NOTIFICATION_TYPES = (("follow", "Follow"),("like", "Like"),("comment", "Comment"),)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="notifications")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="actions")

    type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES
    )

    post = models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient"]),
            models.Index(fields=["is_read"]),
        ]

    def __str__(self):
        return f"{self.actor} -> {self.recipient} ({self.type})"