"""
Сериализаторы для пользователей
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения пользователя"""
    role_name = serializers.CharField(source="role.name", read_only=True)
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "patronymic",
            "full_name",
            "role",
            "role_name",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления пользователя"""
    
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "patronymic",
        ]


class UserListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка пользователей (для админа)"""
    role_name = serializers.CharField(source="role.name", read_only=True)
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "patronymic",
            "full_name",
            "role_name",
            "is_active",
            "created_at",
        ]


