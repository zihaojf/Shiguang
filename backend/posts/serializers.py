from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Post,Like

class PostSerializer(serializers.ModelSerializer):
    publisher = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id','publisher','title','content','likes_count','comments_count','created_at','updated_at','visibility']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id','liker','create_at']

