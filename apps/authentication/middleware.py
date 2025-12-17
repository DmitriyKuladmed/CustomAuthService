"""
Middleware для JWT аутентификации
"""
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from apps.authentication.utils import get_user_id_from_token

User = get_user_model()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware для установки request.user на основе JWT токена
    """
    
    def process_request(self, request):
        """Обработка запроса и установка пользователя"""
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        
        if not auth_header.startswith("Bearer "):
            request.user = None
            return None
        
        token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None
        
        if not token:
            request.user = None
            return None
        
        user_id = get_user_id_from_token(token)
        
        if user_id:
            try:
                user = User.objects.get(id=user_id, is_active=True)
                request.user = user
            except User.DoesNotExist:
                request.user = None
        else:
            request.user = None
        
        return None

