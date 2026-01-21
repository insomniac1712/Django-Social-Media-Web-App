from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.feed, name="feed"),
    path("create/", views.post_create, name="post_create"),
    path("<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("comment/<int:comment_id>/edit/", views.edit_comment, name="comment_edit"),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="comment_delete"),
    path("<int:post_id>/like/", views.toggle_like, name="toggle_like"),
    path("<slug:slug>/post_edit/", views.post_edit, name="post_edit"),
    path("<slug:slug>/delete/", views.post_delete, name="post_delete"),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
