from rest_framework.viewsets import ModelViewSet
from posts.models import Post, Comment
from socialproject.notifications.models import Notification
from .serializers import NotificationSerializer, PostSerializer, CommentSerializer, SimpleUserSerializer
from .permissions import IsOwnnerReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from follow.services import follow_user, unfollow_user
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView, ListAPIView, get_object_or_404
from friendship.models import Follow



# Create your views here.

#Post view
class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related("user")
    serializer_class = PostSerializer
    permission_classes = [IsOwnnerReadOnly]
    lookup_field = 'slug'
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        
#Comment view        
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related("post","posted_by")
    serializer_class = CommentSerializer
    permission_classes = [IsOwnnerReadOnly]
    
User = get_user_model()

#Follow/Unfollow view
class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request,username):
        try:
            target = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail":"User not found"},status=status.HTTP_404_NOT_FOUND)
        
        if not follow_user(request.user, target):
            return Response({"detail":"You cannot follow yourself"},status=status.HTTP_404_NOT_FOUND)
        
        return Response({"detail":f"You are now following {username}","is_following":True}, status=status.HTTP_200_OK)
    
    def delete(self,request, username):
        try:
            target = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail":"User not found"},status =status.HTTP_404_NOT_FOUND)
        
        unfollow_user(request.user,target)
        
        return Response({"detail":f"You unfollowed{username}","is_following":False},status =status.HTTP_200_OK)
    
class FollowersAPIView(ListModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SimpleUserSerializer
    
    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return Follow.objects.followers(user)
    
    def get(self,request, *args, **kwargs): 
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
class FollowingAPIView(ListModelMixin, GenericAPIView):
    serializer_class = SimpleUserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return Follow.objects.following(user)  
    
    def get(self,request, *args, **kwargs):
        return self.list(request, *args, **kwargs) 
    
         
class NotificationListAPIView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).select_related('actor','post').order_by('-created_at')
       
class UnreadNotificationListAPIView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user, is_read=False).select_related('actor','post').order_by('-created_at')

class UnreadNotificationCountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return Response({"unread_count":count})
    
class MarkNotificationAsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self,request, pk):
        notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=['is_read'])
            
        return Response({"detail":"Notification marked as read"})
    
class MarkAllNotificationsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        Notification.objects.filter(recipient=request.user,is_read=False).update(is_read=True)

        return Response({"detail": "All notifications marked as read"})