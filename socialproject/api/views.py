from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from posts.models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnnerReadOnly

# Create your views here.

class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related("user")
    serializer_class = PostSerializer
    permission_classes = [IsOwnnerReadOnly]
    lookup_field = 'slug'
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related("post","posted_by")
    serializer_class = CommentSerializer
    permission_classes = [IsOwnnerReadOnly]