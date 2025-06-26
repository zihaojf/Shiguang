from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate_username(self, value):
        """
        检查用户名是否已存在
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("该用户名已被注册。")
        return value

    def create(self, validated_data):
        # 使用User 模型创建用户
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        # 生成 JWT Token
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'username': user.username,
                'id': user.id
            }
        }