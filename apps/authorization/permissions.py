"""
Permission classes для системы RBAC
"""
from rest_framework import permissions
from rest_framework.request import Request
from apps.authorization.models import BusinessElement, AccessRoleRule


class HasElementPermission(permissions.BasePermission):
    """
    Permission class для проверки доступа к бизнес-элементам
    """
    
    def __init__(self, element_code: str, action: str):
        """
        :param element_code: Код бизнес-элемента (например, 'products', 'orders')
        :param action: Действие ('read', 'create', 'update', 'delete')
        """
        self.element_code = element_code
        self.action = action
    
    def has_permission(self, request: Request, view) -> bool:
        """Проверка прав доступа на уровне запроса"""
        if not request.user or not request.user.is_authenticated:
            return False
        
        if not request.user.role:
            return False
        
        try:
            element = BusinessElement.objects.get(code=self.element_code)
        except BusinessElement.DoesNotExist:
            return False
        
        try:
            rule = AccessRoleRule.objects.get(role=request.user.role, element=element)
        except AccessRoleRule.DoesNotExist:
            return False
        
        # Для чтения проверяем read_permission или read_all_permission
        if self.action == "read":
            return rule.read_permission or rule.read_all_permission
        
        # Для создания проверяем create_permission
        if self.action == "create":
            return rule.create_permission
        
        # Для обновления и удаления проверка будет в has_object_permission
        if self.action in ["update", "delete"]:
            return rule.update_permission or rule.update_all_permission or \
                   rule.delete_permission or rule.delete_all_permission
        
        return False
    
    def has_object_permission(self, request: Request, view, obj) -> bool:
        """Проверка прав доступа на уровне объекта"""
        if not request.user or not request.user.is_authenticated:
            return False
        
        if not request.user.role:
            return False
        
        try:
            element = BusinessElement.objects.get(code=self.element_code)
        except BusinessElement.DoesNotExist:
            return False
        
        try:
            rule = AccessRoleRule.objects.get(role=request.user.role, element=element)
        except AccessRoleRule.DoesNotExist:
            return False
        
        # Проверяем, является ли пользователь владельцем объекта
        is_owner = hasattr(obj, "owner_id") and obj.owner_id == request.user.id
        
        if self.action == "read":
            if is_owner:
                return rule.read_permission or rule.read_all_permission
            return rule.read_all_permission
        
        if self.action == "update":
            if is_owner:
                return rule.update_permission or rule.update_all_permission
            return rule.update_all_permission
        
        if self.action == "delete":
            if is_owner:
                return rule.delete_permission or rule.delete_all_permission
            return rule.delete_all_permission
        
        return False


def get_element_permission(element_code: str, action: str):
    """Фабрика для создания permission классов"""
    return type(
        f"Has{element_code.capitalize()}{action.capitalize()}Permission",
        (HasElementPermission,),
        {},
    )(element_code, action)


class IsAdmin(permissions.BasePermission):
    """Проверка, является ли пользователь администратором"""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role and request.user.role.name == "admin"


