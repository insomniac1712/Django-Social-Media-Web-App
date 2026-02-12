from  friendship.models import Follow
from posts.models import Post


def get_user_feed(user):
    
    following_users = Follow.objects.following(user)
    author_set = set(following_users) | {user}
    posts = Post.objects.filter(user__in=author_set).select_related("user").order_by("-created_at")
    
    return posts
    
    