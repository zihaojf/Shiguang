from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Friendship

class FriendshipSerializer(serializers.ModelSerializer):
    user_a = UserSerializer(read_only=True)
    user_b = UserSerializer(read_only=True)
    class Meta:
        model = Friendship
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')