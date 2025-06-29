from rest_framework import viewsets, status, pagination, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import Friendship
from .serializers import FriendshipSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class FriendshipPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class FriendshipViewSet(viewsets.ModelViewSet):
    serializer_class = FriendshipSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = FriendshipPagination
    queryset = Friendship.objects.all()

    def get_queryset(self):
        return Friendship.objects.filter(
            Q(user_a=self.request.user) | Q(user_b=self.request.user)
        )

    def perform_create(self, serializer):
        user_b_id = self.request.data.get('user_b')

        try:
            user_b = User.objects.get(id=user_b_id)
        except User.DoesNotExist:
            return Response({'detail':'未找到该好友，请确认用户是否存在'},status=status.HTTP_404_NOT_FOUND)

        if self.request.user == user_b:
            raise serializers.ValidationError("不能添加自己为好友")

        existing_request = Friendship.objects.filter(
            Q(user_a=self.request.user,user_b=user_b),status='待确认'
        ).exists()

        existing_friendship = Friendship.objects.filter(
            (Q(user_a=self.request.user,user_b=user_b) | Q(user_a=user_b,user_b=self.request.user)),status='已接受'
        ).exists()

        if existing_friendship:
            raise serializers.ValidationError("你们已经是好友")
        if existing_request:
            raise serializers.ValidationError("你已经向对方发送过请求")

        serializer.save(user_a=self.request.user, user_b=user_b,status='待确认')

    #同意好友请求
    @action(methods=['Post'], detail=True)
    def accept(self, request, pk=None):
        friendship = self.get_object()
        if friendship.user_b != self.request.user:
            return Response({'detail':'没有权限接受该请求'},status=status.HTTP_403_FORBIDDEN)

        if friendship.status != '待确认':
            return Response({'detail':'该请求状态不是待确认'},status=status.HTTP_400_BAD_REQUEST)

        friendship.status='已接受'
        friendship.save()
        #如果有未确认的反向好友请求
        reverse_request = Friendship.objects.filter(
            user_a=friendship.user_b,
            user_b=friendship.user_a,
            status='待确认'
        ).first()

        if reverse_request:
            reverse_request.status='已接受'
            reverse_request.save()
            return Response(FriendshipSerializer(friendship).data)

        #创建反向关系
        Friendship.objects.create(
            user_a=friendship.user_b,
            user_b=friendship.user_a,
            status='已接受',
            remark=''
        )
        return Response(FriendshipSerializer(friendship).data)

    #拒绝好友请求
    @action(methods=['Post'], detail=True)
    def reject(self, request, pk=None):
        friendship = self.get_object()
        if friendship.user_b != self.request.user:
            return Response({'detail':'没有权限拒绝请求'},status=status.HTTP_403_FORBIDDEN)

        if friendship.status !='待确认':
            return Response({'detail':'该请求不是待确认状态'},status=status.HTTP_400_BAD_REQUEST)

        friendship.status='已拒绝'
        friendship.save()
        return Response(FriendshipSerializer(friendship).data)

    #获取当前用户所有好友
    @action(methods=['Get'], detail=False)
    def friends(self, request):
        friendships = Friendship.objects.filter(
            (Q(user_a=self.request.user)),status='已接受'
        )
        page = self.paginate_queryset(friendships)

        if page is not None:
            serializer = FriendshipSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(friendships, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def friend_requests(self, request):
        friendships = Friendship.objects.filter(
            (Q(user_b=self.request.user)),status='待确认'
        )
        page = self.paginate_queryset(friendships)
        if page is not None:
            serializer = FriendshipSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(friendships, many=True)
        return Response(serializer.data)

    @action(methods=['delete'], detail=False)
    def unfriend(self, request):
        """删除好友关系"""
        user_id = self.request.data.get('user_id')

        if not user_id:
            return Response({'detail': '缺少参数 user_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail':'用户不存在'}, status=status.HTTP_404_NOT_FOUND)

        current_user = request.user

        if current_user.id == user_id:
            return Response({'detail': '不能删除自己'}, status=status.HTTP_400_BAD_REQUEST)

        # 查找正向和反向记录
        forward = Friendship.objects.filter(
            user_a=current_user.id,
            user_b=user.id,
            status='已接受'
        ).first()

        reverse = Friendship.objects.filter(
            user_a=user.id,
            user_b=current_user.id,
            status='已接受'
        ).first()

        if not forward and not reverse:
            return Response({'detail': '你们目前不是好友关系'}, status=status.HTTP_400_BAD_REQUEST)

        if forward:
            forward.delete()
        if reverse:
            reverse.delete()

        return Response({'detail': '好友关系已删除'}, status=status.HTTP_200_OK)





