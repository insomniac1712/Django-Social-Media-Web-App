from rest_framework import serializers
from posts.models import Post, Comment, Like


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id','user','title','caption','image','slug','created_at',]
        read_only_fields = ["id", "slug", "created_at"]
        

class CommentSerializer(serializers.ModelSerializer):
    posted_by = serializers.StringRelatedField(read_only=True)
    post = serializers.SlugRelatedField(queryset=Post.objects.all(),slug_field='slug')
    
    class Meta:
        model = Comment
        fields = ['id','post','posted_by','body','created_at','updated_at']
        read_only_fields = ['id','posted_by','created_at','updated_at']