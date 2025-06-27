from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Post,Like
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(publisher=self.request.user)

    @action(detail=True,methods=['POST'])
    def like(self,request,pk=None):
        post = self.get_object()
        user = request.user
        if Like.objects.filter(post=post,liker=user).exists():
            return Response({'detail':'你已经点过赞了'},status=status.HTTP_400_BAD_REQUEST)

        Like.objects.create(post=post,liker=user)
        return Response({'detail':'点赞成功'},status=status.HTTP_201_CREATED)
    @action(detail=True,methods=['DELETE'])
    def unlike(self,request,pk=None):
        post = self.get_object()
        user = request.user

        like = Like.objects.filter(post=post,liker=user)
        if not like.exists():
            return Response({'detail':'你还没有点过赞'},status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response({'detail':'取消点赞成功'},status=status.HTTP_200_OK)


