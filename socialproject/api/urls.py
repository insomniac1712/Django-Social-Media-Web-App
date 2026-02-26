from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FollowersAPIView, FollowingAPIView, MarkAllNotificationsReadAPIView, MarkNotificationAsReadAPIView, NotificationListAPIView, PostViewSet, CommentViewSet, FollowAPIView, UnreadNotificationCountAPIView, UnreadNotificationListAPIView

router = DefaultRouter()
router.register('posts',PostViewSet, basename='posts')
router.register('comments', CommentViewSet, basename='comments')

urlpatterns = router.urls
urlpatterns +=[
    path("users/<str:username>/follow/",FollowAPIView.as_view()),
    path("users/<str:username>/following/",FollowingAPIView.as_view()),
    path("users/<str:username>/followers/",FollowersAPIView.as_view()),
    path("notifications/", NotificationListAPIView.as_view()),
    path("notifications/unread/", UnreadNotificationListAPIView.as_view()),
    path("notifications/unread-count/", UnreadNotificationCountAPIView.as_view()),
    path("notifications/<int:pk>/read/", MarkNotificationAsReadAPIView.as_view()),
    path("notifications/mark-all-read/", MarkAllNotificationsReadAPIView.as_view()),
]

