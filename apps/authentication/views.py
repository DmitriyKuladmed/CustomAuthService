"""
Views для аутентификации
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apps.authentication.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    TokenRefreshSerializer,
)
from apps.authentication.utils import (
    generate_access_token,
    generate_refresh_token,
    decode_token,
)

User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """Регистрация нового пользователя"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        access_token = generate_access_token(user.id)
        refresh_token = generate_refresh_token(user.id)
        
        return Response(
            {
                "message": "Пользователь успешно зарегистрирован",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """Вход в систему"""
    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]
    
    try:
        user = User.objects.get(email=email, is_active=True)
    except User.DoesNotExist:
        return Response(
            {"error": "Неверный email или пароль"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    
    if not user.check_password(password):
        return Response(
            {"error": "Неверный email или пароль"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    
    access_token = generate_access_token(user.id)
    refresh_token = generate_refresh_token(user.id)
    
    return Response(
        {
            "message": "Успешный вход в систему",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token_view(request):
    """Обновление access токена"""
    serializer = TokenRefreshSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    refresh_token = serializer.validated_data["refresh_token"]
    payload = decode_token(refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        return Response(
            {"error": "Неверный refresh токен"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    
    user_id = payload.get("user_id")
    try:
        user = User.objects.get(id=user_id, is_active=True)
    except User.DoesNotExist:
        return Response(
            {"error": "Пользователь не найден"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    
    access_token = generate_access_token(user.id)
    
    return Response(
        {
            "access_token": access_token,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def logout(request):
    """Выход из системы"""
    # В простой реализации JWT logout не требует действий на сервере
    # Токен инвалидируется на клиенте
    # В production можно использовать blacklist токенов
    return Response(
        {"message": "Успешный выход из системы"},
        status=status.HTTP_200_OK,
    )
