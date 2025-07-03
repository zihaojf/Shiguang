from rest_framework import serializers
from .models import Comment
from users.serializers import UserSerializer
from posts.serializers import PostSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    parent_comment = "self"  # 展示完整父评论信息
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'post', 'parent_comment', 'children', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def get_children(self, obj):
        if hasattr(obj, 'children') and obj.children.exists():
            return CommentSerializer(obj.children.all(), many=True,context=self.context).data
        return []