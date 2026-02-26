from rest_framework import serializers
from posts.models import Post, Comment
from django.contrib.auth import get_user_model
from notifications.models import Notification


User = get_user_model()


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
        
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id','username']
        
        
class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.CharField(source='actor.username')
    post_slug = serializers.CharField(source='post.slug', allow_null=True)
    message = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id','actor','type','post_slug','message','created_at']
    
    def get_message(self, obj):
        if obj.type == 'follow':
            return f"{obj.actor.username} followed you."
        if obj.type == 'like':
            return f"{obj.actor.username} liked your post."
        if obj.type == 'comment':
            return f"{obj.actor.username} commented on your post."
        return ""