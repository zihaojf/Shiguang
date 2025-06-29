from rest_framework.decorators import action
from rest_framework import viewsets,status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from posts.models import Post
from .serializers import CommentSerializer
from .models import Comment
from friendship.models import Friendship

class CommentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        parent_comment_id = self.request.data.get('parent_comment')
        parent_comment = None

        if not post_id:
            raise ValidationError({'post': '帖子ID不能为空'})

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise ValidationError({'post': '未找到该帖子'})

        # 权限控制
        if post.publisher != self.request.user:
            if post.publisher.profile_visibility == 'privacy':
                raise ValidationError({'post': '未找到该帖子'})

            if post.visibility != 'public':
                from friendship.models import Friendship
                is_friend = Friendship.objects.filter(
                    user_a=post.publisher,
                    user_b=self.request.user,
                    status='已接受'
                ).exists()
                if not is_friend:
                    raise ValidationError({'post': '未找到该帖子'})

        if parent_comment_id:
            try:
                parent_comment = Comment.objects.get(id=parent_comment_id)
            except Comment.DoesNotExist:
                raise ValidationError({'parent_comment': '未找到父评论'})

            if parent_comment.post.id != post.id:
                raise ValidationError({'parent_comment': '父评论与帖子不匹配'})

        serializer.save(user=self.request.user, post=post, parent_comment=parent_comment)

    def list(self, request, *args, **kwargs):
        post_id = request.query_params.get('post')
        if not post_id:
            return Response(
                {'detail': '缺少 post 参数'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail':'未找到该帖子'},status=status.HTTP_404_NOT_FOUND)

        # 权限控制
        if not post.publisher == request.user:
            if post.publisher.profile_visibility == 'privacy':
                return Response({'detail':'未找到该帖子'},status=status.HTTP_404_NOT_FOUND)
            if post.visibility != 'public':
                is_friend = Friendship.objects.filter(
                    user_a=post.publisher,
                    user_b=request.user,
                    status='已接受'
                ).exists()
                if not is_friend:
                    return Response({'detail':'未找到该帖子'},status=status.HTTP_404_NOT_FOUND)

        queryset = Comment.objects.filter(post=post, parent_comment=None).order_by('-created_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
