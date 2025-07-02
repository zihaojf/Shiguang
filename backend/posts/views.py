from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from urllib3 import request

from .models import Post,Like
from .serializers import PostSerializer, LikeSerializer
from friendship.models import Friendship
from django.db.models import Q

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        # like/unlike 时我们需要直接拿到任意 post
        if self.action in ['like', 'unlike']:
            return Post.objects.all()

        user = self.request.user
        if not user.is_authenticated:
            return Post.objects.filter(visibility='public')

        # 获取当前用户能看到的帖子
        friends = Friendship.objects.filter(
            (Q(user_a=user, status='已接受'))
        ).values_list('user_b')

        friend_ids = set()
        for b in friends:
            if b != user.id:
                friend_ids.add(b)

        queryset = Post.objects.all()
        # 查询逻辑说明：
        # 自己发布的帖子
        # 发布者是好友且帖子是 public/friend
        # 发布者不是好友但帖子是 public
        # 发布者是隐私账号（privacy） ->只能自己看
        return queryset.filter(
            Q(publisher=user) |
            (
                    Q(publisher__profile_visibility='public') &
                    Q(visibility='public')
            ) |
            (
                    Q(publisher__in=friend_ids) & ~Q(publisher__profile_visibility='privacy') &
                    (Q(visibility='public') | Q(visibility='friend'))
            )
        )

    def perform_create(self, serializer):
        serializer.save(publisher=self.request.user)

    @action(detail=True,methods=['POST'])
    def like(self,request,pk=None):
        post = self.get_object()
        user = request.user
        publisher = post.publisher

        # 1. 如果发布者是隐私账户，只允许自己点赞
        if not post.publisher == self.request.user:
            if publisher.profile_visibility == 'privacy' and publisher != user:
                return Response({'detail': '该用户设置了私密账户，你不能操作'}, status=status.HTTP_403_FORBIDDEN)

            # 2. 如果发布者是好友账户或帖子是好友可见，则必须是好友
            if publisher.profile_visibility == 'friend' or post.visibility == 'friend':
                is_friend = Friendship.objects.filter(
                    (Q(user_a=publisher, user_b=user, status='已接受'))
                ).exists()

                if not is_friend:
                    return Response({'detail': '你需要先添加对方为好友才能点赞'}, status=status.HTTP_403_FORBIDDEN)

        if Like.objects.filter(post=post,liker=user).exists():
            return Response({'detail':'你已经点过赞了'},status=status.HTTP_400_BAD_REQUEST)

        Like.objects.create(post=post,liker=user)
        return Response({'detail':'点赞成功'},status=status.HTTP_201_CREATED)
    @action(detail=True,methods=['DELETE'])
    def unlike(self,request,pk=None):
        post = self.get_object()
        user = request.user
        publisher = post.publisher

        if not post.publisher == self.request.user:
            # 1. 如果发布者是隐私账户，只允许自己点赞
            if publisher.profile_visibility == 'privacy' and publisher != user:
                return Response({'detail': '该用户设置了私密账户，你不能操作'}, status=status.HTTP_403_FORBIDDEN)

            # 2. 如果发布者是好友账户或帖子是好友可见，则必须是好友
            if publisher.profile_visibility == 'friend' or post.visibility == 'friend':
                is_friend = Friendship.objects.filter(
                    (Q(user_a=publisher, user_b=user, status='已接受'))
                ).exists()

                if not is_friend:
                    return Response({'detail': '你需要先添加对方为好友才能取消点赞'}, status=status.HTTP_403_FORBIDDEN)

        like = Like.objects.filter(post=post,liker=user)
        if not like.exists():
            return Response({'detail':'你还没有点过赞'},status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response({'detail':'取消点赞成功'},status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def check_like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        # 检查用户是否登录
        if not user.is_authenticated:
            return Response({'detail': '需要登录才能查看点赞状态'}, status=status.HTTP_401_UNAUTHORIZED)

        publisher = post.publisher

        # 权限判断（和 like/unlike 一致）
        if publisher.profile_visibility == 'privacy' and publisher != user:
            return Response({'detail': '该用户设置了私密账户，你不能查看'}, status=status.HTTP_403_FORBIDDEN)

        if (publisher.profile_visibility == 'friend' or post.visibility == 'friend') and publisher != user:
            is_friend = Friendship.objects.filter(
                Q(user_a=publisher, user_b=user, status='已接受')
            ).exists()
            if not is_friend:
                return Response({'detail': '你需要是好友才能查看点赞状态'}, status=status.HTTP_403_FORBIDDEN)

        is_liked = Like.objects.filter(post=post, liker=user).exists()
        return Response({'is_liked': is_liked}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def mylikes(self, request):
        user = request.user
        # 检查用户是否登录
        if not user.is_authenticated:
            return Response({'detail': '需要登录才能查看他人点赞情况'}, status=status.HTTP_401_UNAUTHORIZED)

        queryset = Like.objects.filter(post__user=user).order_by('-created_at')
        serializer = LikeSerializer(queryset, many=True)
        return Response(serializer.data)


