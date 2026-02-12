from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,login,get_user_model
from .forms import LoginForm, UserRegisterationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import UserEditForm, ProfileEditForm
from posts.models import Post, Like
from posts.forms import CommentForm
from follow.services import is_following, followers_count, following_count
from friendship.models import Follow
from django.db.models import Count
from django.core.paginator import Paginator

User = get_user_model()

#Login view
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,username = data['username'], password = data['password'])
            if user is not None:
                login(request,user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                
                return redirect("posts:feed")
            else:
                return render(request, 'users/login.html', {'form': form, 'error': "Invalid credentials"})
    else:
        form = LoginForm()
    return render(request,'users/login.html',{'form':form})


#Page after login to show user profile and posts
@login_required
def profile(request,username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=profile_user).prefetch_related("comments").annotate(like_count=Count("likes"))
    liked_post_ids = set(Like.objects.filter(user=request.user).values_list("post_id", flat=True))
    profile = Profile.objects.filter(user=profile_user).first()
    return render(request, 'users/profile.html', 
                  {'posts': posts, 
                   'profile': profile,
                   'profile_user':profile_user,
                   'liked_post_ids': liked_post_ids,
                   'comment_form_class': CommentForm,
                   'is_following':(is_following(request.user, profile_user) if request.user != profile_user else False),
                   'followers_count':followers_count(profile_user),
                   'following_count':following_count(profile_user),
                   })
    
@login_required
def my_profile(request):
    return redirect('users:profile', username=request.user.username)


#User registeration page
def register(request):
    if request.method == 'POST':
        user_form = UserRegisterationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'users/register_done.html')
    else:
        user_form = UserRegisterationForm()
    return render(request,'users/register.html', {'user_form':user_form})

#Profile edit page
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('users:profile', username=request.user.username)
    else:
        user_form = UserEditForm(
            instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile, files=request.FILES)
    return render(request, 'users/edit.html', {'user_form':user_form, 'profile_form':profile_form})


@login_required
def followers_list(request, username):
    target = get_object_or_404(User, username=username)
    followers = Follow.objects.followers(target)
    return render(request, 'users/followers_list.html', {'profile_user':target, 'followers':followers})

@login_required
def following_list(request, username):
    target = get_object_or_404(User, username=username)
    following = Follow.objects.following(target)
    return render(request, 'users/following_list.html', {'profile_user':target, 'following':following})

@login_required
def search_users(request):
    query = request.GET.get("q", "").strip()
    users = User.objects.none()
    
    if query:
        users = (User.objects.filter(username__icontains = query).exclude(id=request.user.id)).select_related("profile").annotate(followers_count=Count("followers")).order_by("-followers_count")
    
    paginator = Paginator(users,10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "users/search_results.html",{
        "users":users,"query":query, "page_obj":page_obj
    })
