from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    parent_comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), allow_null=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'post', 'parent_comment', 'children', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def get_children(self, obj):
        if hasattr(obj, 'children') and obj.children.exists():
            return CommentSerializer(obj.children.all(), many=True).data
        return []