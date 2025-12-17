"""
Views для пользователей
"""
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from apps.authorization.permissions import IsAdmin
from apps.users.serializers import (
    UserSerializer,
    UserUpdateSerializer,
    UserListSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с пользователями"""
    queryset = User.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_permissions(self):
        """Разные права для разных действий"""
        if self.action in ["list", "retrieve"]:
            return [IsAdmin()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=["get", "patch", "delete"])
    def me(self, request):
        """Получение, обновление или удаление текущего пользователя"""
        user = request.user
        
        if request.method == "GET":
            serializer = UserSerializer(user)
            return Response(serializer.data)
        
        elif request.method == "PATCH":
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response_serializer = UserSerializer(user)
                return Response(response_serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == "DELETE":
            # Мягкое удаление
            user.is_active = False
            user.save()
            return Response(
                {"message": "Аккаунт успешно удален"},
                status=status.HTTP_200_OK,
            )
    
    def list(self, request, *args, **kwargs):
        """Список пользователей (только для админа)"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Детали пользователя (только для админа)"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
