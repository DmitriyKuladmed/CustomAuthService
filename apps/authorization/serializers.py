"""
Сериализаторы для авторизации
"""
from rest_framework import serializers
from apps.authorization.models import Role, BusinessElement, AccessRoleRule


class RoleSerializer(serializers.ModelSerializer):
    """Сериализатор для ролей"""
    
    class Meta:
        model = Role
        fields = ["id", "name", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class BusinessElementSerializer(serializers.ModelSerializer):
    """Сериализатор для бизнес-объектов"""
    
    class Meta:
        model = BusinessElement
        fields = ["id", "code", "name", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class AccessRoleRuleSerializer(serializers.ModelSerializer):
    """Сериализатор для правил доступа"""
    role_name = serializers.CharField(source="role.name", read_only=True)
    element_code = serializers.CharField(source="element.code", read_only=True)
    element_name = serializers.CharField(source="element.name", read_only=True)
    
    class Meta:
        model = AccessRoleRule
        fields = [
            "id",
            "role",
            "role_name",
            "element",
            "element_code",
            "element_name",
            "read_permission",
            "read_all_permission",
            "create_permission",
            "update_permission",
            "update_all_permission",
            "delete_permission",
            "delete_all_permission",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class AccessRoleRuleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания правил доступа"""
    
    class Meta:
        model = AccessRoleRule
        fields = [
            "role",
            "element",
            "read_permission",
            "read_all_permission",
            "create_permission",
            "update_permission",
            "update_all_permission",
            "delete_permission",
            "delete_all_permission",
        ]

