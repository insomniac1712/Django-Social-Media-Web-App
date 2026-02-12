from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from feed.selectors import get_user_feed
from django.db.models import Count

from posts.forms import CommentForm
from posts.models import Like
# Create your views here.

@login_required
def feed_view(request):
    post_qs = get_user_feed(request.user).prefetch_related("comments","comments__posted_by").annotate(like_count=Count("likes")) 
    paginator = Paginator(post_qs, 5)
    page_obj = paginator.get_page(request.GET.get('page'))
    liked_post_ids = set(Like.objects.filter(user=request.user).values_list("post_id", flat=True))
    return render(request, 'feed/feed.html', 
                  {'posts': page_obj, "liked_post_ids": liked_post_ids, "page_obj": page_obj, "comment_form_class":CommentForm})