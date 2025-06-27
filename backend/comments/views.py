from rest_framework.decorators import action
from rest_framework import viewsets,status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from posts.models import Post
from .serializers import CommentSerializer
from .models import Comment

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self,serializer):
        post_id = self.request.data['post']
        parent_comment_id = self.request.data.get('parent_comment')
        parent_comment = None
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail':'未找到该帖子'},status=status.HTTP_404_NOT_FOUND)

        if parent_comment_id :
            try:
                parent_comment = Comment.objects.get(id=parent_comment_id)
            except Comment.DoesNotExist:
                return Response({'detail':'未找到父评论'},status=status.HTTP_404_NOT_FOUND)
        serializer.save(user=self.request.user,post=post,parent_comment=parent_comment)

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

        queryset = Comment.objects.filter(post=post, parent_comment=None)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
