from friendship.models import Follow
from django.contrib.auth import get_user_model

User = get_user_model()

def follow_user(user, target_user):
    if user==target_user:
        return False
    Follow.objects.follow(user,target_user)
    return True
    
def unfollow_user(user, target_user):
    Follow.objects.unfollow(user, target_user)
    return True

def is_following(user, target_user):
    return Follow.objects.follows(user,target_user)

def followers_count(user):
    return len(Follow.objects.followers(user))

def following_count(user):
    return len(Follow.objects.following(user))

