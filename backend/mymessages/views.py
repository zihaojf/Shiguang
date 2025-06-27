
from rest_framework import status,viewsets
from rest_framework.response import Response
from .models import Group,GroupMember,Message
from .serializers import GroupSerializer, GroupMemberSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.conf import  settings

User = settings.AUTH_USER_MODEL

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)


class GroupMemberViewSet(viewsets.ModelViewSet):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer
    permission_classes = (IsAuthenticated,)



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        #接收者
        receiver_id = self.request.data['receiver']
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({'detail':'未找到消息接收者'},status=status.HTTP_404_NOT_FOUND)

        group_id = self.request.data.get('group_id')
        # 群聊
        if group_id:
            try:
                group = Group.objects.get(id=group_id)
            except Group.DoesNotExist:
                return Response({'detail':'未找到该群聊'},status.HTTP_404_NOT_FOUND)

        else :
            group = None

        serializer.save(sender=settings.AUTH_USER_MODEL, receiver=receiver, group=group)



