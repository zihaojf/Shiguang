from rest_framework import viewsets, permissions, status
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django.db.models import Q
from django.contrib.auth.password_validation import validate_password

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 所有用户都可以看到全部用户列表
        return User.objects.all()

    def get_object(self):
        obj = super().get_object()
        if self.request.method in ["PUT", "PATCH","DELETE"]:
            if obj != self.request.user:
                raise PermissionDenied("您只能修改或删除自己的账户信息。")
            return obj
        return obj

    @action(detail=False, methods=['get', 'put'], url_path='me', url_name='me')
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = self.get_serializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='search', permission_classes=[permissions.AllowAny])
    def search_users(self, request):
        query = request.query_params.get('q','')
        if not query:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(Q(username__icontains=query) | Q(nickname__icontains=query)).exclude(id=request.user.id)[:50]
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='change_password', permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response({"detail": "必须提供旧密码和新密码。"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({"detail": "旧密码错误。"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password, user)
        except Exception as e:
            return Response({"detail": e.args}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "密码修改成功。"}, status=status.HTTP_200_OK)

