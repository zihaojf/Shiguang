from rest_framework import viewsets, permissions, status
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

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