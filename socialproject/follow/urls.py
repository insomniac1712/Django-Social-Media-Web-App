from django.urls import path

from .views import follow_view, unfollow_view, toggle_follow

app_name='follow'

urlpatterns = [
    path("follow/<str:username>/", follow_view, name="follow"),
    path("unfollow/<str:username>/",unfollow_view, name="unfollow"),
    path("toggle/<str:username>/", toggle_follow, name="toggle"),

]
