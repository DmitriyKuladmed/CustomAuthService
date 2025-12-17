"""
URLs для управления авторизацией (Admin API)
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.authorization import views

router = DefaultRouter()
router.register(r"roles", views.RoleViewSet, basename="role")
router.register(r"elements", views.BusinessElementViewSet, basename="element")
router.register(r"rules", views.AccessRoleRuleViewSet, basename="rule")
router.register(r"users", views.UserRoleViewSet, basename="user-role")

urlpatterns = [
    path("", include(router.urls)),
]

