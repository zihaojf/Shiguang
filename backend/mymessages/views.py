
from django.db.models import Q,Max
from rest_framework import status,viewsets
from rest_framework.response import Response
from .models import Group,GroupMember,Message
from .serializers import GroupsSerializer, GroupMembersSerializer, MessagesSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from users.serializers import UserSerializer

User = get_user_model()

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer
    permission_classes = (IsAuthenticated,)


class GroupMemberViewSet(viewsets.ModelViewSet):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMembersSerializer
    permission_classes = (IsAuthenticated,)



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessagesSerializer
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
                group = Group.objects.filter(id=group_id)
            except Group.DoesNotExist:
                return Response({'detail':'未找到该群聊'},status.HTTP_404_NOT_FOUND)

        else :
            group = None

        serializer.save(sender=self.request.user, receiver=receiver, group=group)
    @action(methods=['get'],detail=False)
    def get_list(self, request):
        user = request.user

        messages = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-created_at')
        contacts = {}

        for msg in messages:
            contact = msg.receiver if msg.sender == self.request.user else msg.receiver
            if contact.id not in contacts:
                contacts[contact.id] = {
                    'contact_id': contact.id,
                    'contact_username': contact.username,
                    'last_message':msg.content,
                    'last_time':msg.created_at
                }
        sorted_contacts = sorted(contacts.values(), key=lambda x: x['last_time'], reverse=True)
        return Response(sorted_contacts)





    @action(methods=['get'],detail=False)
    def get_detail(self,request):
        user = self.request.user

        contact_id = request.query_params.get('contact_id')
        if not contact_id:
            return Response({'detail':'缺少contact_id'},status=status.HTTP_404_NOT_FOUND)
        try:
            contact = User.objects.get(id=contact_id)
        except User.DoesNotExist:
            return Response({'detail':'联系人不存在'},status=status.HTTP_404_NOT_FOUND)

        messages = Message.objects.filter(
            Q(sender=user, receiver=contact) | Q(sender=contact,receiver=user)
        ).order_by('-created_at')

        serializer = MessagesSerializer(messages, many=True)
        return Response(serializer.data)





