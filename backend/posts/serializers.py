from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Post,Like
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    publisher = UserSerializer(read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id','publisher','title','content','likes','comments','created_at','updated_at','visibility']

    def get_like(self,obj):
        return obj.likes

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id','liker','create_at']

