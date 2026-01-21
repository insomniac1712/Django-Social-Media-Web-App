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
            return redirect('posts:feed')
    else:
        form = PostCreateForm()
    return render(request, 'posts/create.html',{'form':form})


#feeds
@login_required
def feed(request):
    
    
    posts = (Post.objects.select_related('user').prefetch_related('comments').annotate(like_count=Count('likes')) )
    
    paginator = Paginator(posts, 5) 
    page_obj = paginator.get_page(request.GET.get('page'))
    
    liked_post_ids = set(Like.objects.filter(user=request.user).values_list("post_id", flat=True))
    
    comment_form_class = CommentForm
    return render(request,'posts/feed.html',
                  {'posts':page_obj, 'comment_form_class':CommentForm, "page_obj": page_obj,"liked_post_ids": liked_post_ids},)


#add comment
@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.posted_by = request.user
        comment.save()
        
    return redirect('posts:feed')


#delete comment
@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if not user_owns_comment(request.user, comment):
        return HttpResponseForbidden("Only original poster can delete comments.")
    
    comment.delete()
    return redirect('posts:feed')

#edit comment
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if not user_owns_comment(request.user, comment):
        return HttpResponseForbidden("Only original poster can edit comments.")
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('posts:feed')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'posts/comment_edit.html', {'form': form, 'comment': comment})

@login_required
@require_POST
@transaction.atomic
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    like, created = Like.objects.get_or_create(
        user=request.user, post=post)
    
    if not created:
        like.delete()
 
    return redirect('posts:feed')


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
    return redirect("posts:feed")