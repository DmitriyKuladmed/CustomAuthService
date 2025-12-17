import uuid
import bcrypt
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from apps.authorization.models import Role


class UserManager(BaseUserManager):
    """Менеджер для модели User"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Создание обычного пользователя"""
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создание суперпользователя"""
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    """Кастомная модель пользователя"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name="Email")
    password = models.CharField(max_length=255, verbose_name="Хеш пароля")
    
    # Персональные данные
    first_name = models.CharField(max_length=100, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    
    # Роль пользователя
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="Роль"
    )
    
    # Статус
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    
    # Даты
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.email
    
    def set_password(self, raw_password):
        """Хеширование пароля с помощью bcrypt"""
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(raw_password.encode("utf-8"), salt).decode("utf-8")
    
    def check_password(self, raw_password):
        """Проверка пароля"""
        try:
            return bcrypt.checkpw(
                raw_password.encode("utf-8"),
                self.password.encode("utf-8")
            )
        except (AttributeError, ValueError):
            return False
    
    @property
    def is_authenticated(self):
        """Всегда True для активных пользователей"""
        return self.is_active
    
    @property
    def full_name(self):
        """Полное имя пользователя"""
        parts = [self.last_name, self.first_name, self.patronymic]
        return " ".join(filter(None, parts)) or self.email
