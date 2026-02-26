from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostCreateForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Post,Like,Comment 
from django.db import transaction
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST

# Create your views here.

def user_owns_post(user, post):
    return post.user == user

def user_owns_comment(user, comment):
    return comment.posted_by == user

#create post
@login_required
def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST,request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return redirect('feed:feed')
    else:
        form = PostCreateForm()
    return render(request, 'posts/create.html',{'form':form})


#feeds
@login_required
def feed(request):
    return redirect('feed:feed')


#add comment
@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    show_comment_actions = request.POST.get("show_comment_actions") == "1"

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.posted_by = request.user
        comment.save()

    return render(
        request,
        "posts/comment_section.html",
        {
            "post": post,
            "comment_form_class": CommentForm,
            "show_comment_actions": show_comment_actions,
        }
    )



#delete comment
@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    show_comment_actions = request.POST.get("show_comment_actions") == "1"

    if request.user != comment.posted_by:
        return HttpResponseForbidden()

    comment.delete()

    return render(
        request,
        "posts/comment_section.html",
        {
            "post": post,
            "comment_form_class": CommentForm,
            "show_comment_actions": show_comment_actions,
        }
    )

#edit comment
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    show_comment_actions = request.POST.get("show_comment_actions") == "1"
    
    if not user_owns_comment(request.user, comment):
        return HttpResponseForbidden("Only original poster can edit comments.")
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
        return render(
            request,
            "posts/comment_section.html",
            {
                "post": post,
                "comment_form_class": CommentForm,
                "show_comment_actions": show_comment_actions,
            }
        )
    else:
        form = CommentForm(instance=comment)
    return render(request, 'posts/comment_edit.html', {'form': form, 'comment': comment})

@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    liked = Like.objects.filter(user=request.user, post=post).exists()

    if liked:
        Like.objects.filter(user=request.user, post=post).delete()
    else:
        Like.objects.get_or_create(user=request.user, post=post)

    context = {
        "post": post,
        "is_liked": not liked,
        "like_count": Like.objects.filter(post=post).count(),
    }

    return render(request, "posts/like_section.html", context)


@login_required
def post_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related("user").prefetch_related("comments","likes"), slug=slug)
    liked_post_ids = set(Like.objects.filter(user=request.user).values_list("post_id", flat=True))
    return render(request, 'posts/detail.html', {'post': post, "liked_post_ids": liked_post_ids,"comment_form_class": CommentForm})


@login_required
def post_edit(request,slug):
    post = get_object_or_404(Post, slug=slug)
    if not user_owns_post(request.user,post):
        return HttpResponseForbidden("Only original poster can edit posts.")    
    
    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts:post_detail",slug=post.slug)
    else:
        form = PostCreateForm(instance=post)
        
    return render(request, "posts/edit.html",{"post":post,"form":form})
  
  
@login_required
@require_POST
def post_delete(request,slug):
    post = get_object_or_404(Post, slug=slug)
    if not user_owns_post(request.user,post):
        return HttpResponseForbidden("Only original poster can delete posts.")
    
    post.delete()
    return redirect("feed:feed")
