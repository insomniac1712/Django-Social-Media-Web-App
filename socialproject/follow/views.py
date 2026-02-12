from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .services import follow_user, unfollow_user
from .services import followers_count, following_count
from friendship.models import Follow
from django.contrib.auth.models import User


# Create your views here.

User = get_user_model()

@login_required
def follow_view(request, username):
    target = get_object_or_404(User, username=username)
    follow_user(request.user, target)
    return redirect("profile", username=username)

@login_required
def unfollow_view(request, username):
    target = get_object_or_404(User, username=username)
    unfollow_user(request.user, target)
    return redirect("profile", username=username)
    
    
@login_required
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)
    
    if Follow.objects.follows(request.user, target):
        Follow.objects.remove_follower(request.user, target)
    else:
        Follow.objects.add_follower(request.user, target)

    context = {
        "profile_user": target,
        "is_following": Follow.objects.follows(request.user, target),
        "followers_count": followers_count(target),
        "following_count": following_count(target),
    }

    return render(request, "follow/follow_section.html", context)
