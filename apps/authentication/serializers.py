"""
Сериализаторы для аутентификации
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.authorization.models import Role

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ["email", "password", "password_confirm", "first_name", "last_name", "patronymic"]
    
    def validate(self, attrs):
        """Валидация паролей"""
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Пароли не совпадают"})
        return attrs
    
    def create(self, validated_data):
        """Создание пользователя"""
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """Сериализатор для входа в систему"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class TokenRefreshSerializer(serializers.Serializer):
    """Сериализатор для обновления токена"""
    refresh_token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения пользователя"""
    role_name = serializers.CharField(source="role.name", read_only=True)
    
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "patronymic",
            "role",
            "role_name",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

