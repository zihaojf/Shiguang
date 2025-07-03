from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Post,Like

class PostSerializer(serializers.ModelSerializer):
    publisher = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id','publisher','title','content','image','likes_count','comments_count','created_at','updated_at','visibility']
        ordering='-created_at'

    def validate_image(self, value):
        """
        验证图片格式是否为允许的类型
        """
        if value:
            allowed_types = ['image/jpeg', 'image/png']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError("仅支持 JPG/PNG 格式的图片")
        return value

class LikeSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    liker = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id','liker','post','create_at']

