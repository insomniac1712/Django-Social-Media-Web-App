from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from friendship.models import Follow
from posts.models import Like

@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        if instance.follower!=instance.followee:
            Notification.objects.create(recipient=instance.followee, actor = instance.follower, type ='follow')
            
            
@receiver(post_save, sender=Like)
def create_like_notification(sender, instance ,created, **kwargs):
    if created:
        post = instance.post
        actor = instance.user
        recipient = post.user
        
        if actor!=recipient:
            Notification.objects.create(recipient=recipient, actor=actor,type='like',post=post)