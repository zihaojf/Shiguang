from rest_framework import viewsets, permissions, status
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action

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