"""
Views для управления авторизацией (Admin API)
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from apps.authorization.models import Role, BusinessElement, AccessRoleRule
from apps.authorization.permissions import IsAdmin
from apps.authorization.serializers import (
    RoleSerializer,
    BusinessElementSerializer,
    AccessRoleRuleSerializer,
    AccessRoleRuleCreateSerializer,
)

User = get_user_model()


class RoleViewSet(viewsets.ModelViewSet):
    """ViewSet для управления ролями"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class BusinessElementViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра бизнес-объектов"""
    queryset = BusinessElement.objects.all()
    serializer_class = BusinessElementSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class AccessRoleRuleViewSet(viewsets.ModelViewSet):
    """ViewSet для управления правилами доступа"""
    queryset = AccessRoleRule.objects.select_related("role", "element").all()
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get_serializer_class(self):
        if self.action == "create":
            return AccessRoleRuleCreateSerializer
        return AccessRoleRuleSerializer
    
    def list(self, request, *args, **kwargs):
        """Список правил доступа с фильтрацией"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # Фильтрация по роли
        role_id = request.query_params.get("role_id")
        if role_id:
            queryset = queryset.filter(role_id=role_id)
        
        # Фильтрация по элементу
        element_id = request.query_params.get("element_id")
        if element_id:
            queryset = queryset.filter(element_id=element_id)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserRoleViewSet(viewsets.ViewSet):
    """ViewSet для управления ролями пользователей"""
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @action(detail=True, methods=["patch"])
    def assign_role(self, request, pk=None):
        """Назначение роли пользователю"""
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        role_id = request.data.get("role_id")
        if not role_id:
            return Response(
                {"error": "role_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            role = Role.objects.get(pk=role_id)
        except Role.DoesNotExist:
            return Response(
                {"error": "Роль не найдена"},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        user.role = role
        user.save()
        
        from apps.users.serializers import UserSerializer
        serializer = UserSerializer(user)
        return Response(serializer.data)
