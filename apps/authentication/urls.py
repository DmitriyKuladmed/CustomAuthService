"""
URLs для аутентификации
"""
from django.urls import path
from apps.authentication import views

app_name = "authentication"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("refresh/", views.refresh_token_view, name="refresh"),
]


