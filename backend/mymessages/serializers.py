from rest_framework import serializers
from .models import Group,GroupMember,Message
from users.serializers import UserSerializer

class GroupsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'

class GroupMembersSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupMember
        fields = '__all__'

class MessagesSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = '__all__'


