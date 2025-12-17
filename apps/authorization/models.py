from django.db import models


class Role(models.Model):
    """Роли пользователей в системе"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Название роли")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"
        ordering = ["name"]

    def __str__(self):
        return self.name


class BusinessElement(models.Model):
    """Бизнес-объекты приложения, к которым применяется система доступа"""
    code = models.CharField(max_length=50, unique=True, verbose_name="Код объекта")
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Бизнес-объект"
        verbose_name_plural = "Бизнес-объекты"
        ordering = ["code"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class AccessRoleRule(models.Model):
    """Правила доступа ролей к бизнес-объектам"""
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="access_rules",
        verbose_name="Роль"
    )
    element = models.ForeignKey(
        BusinessElement,
        on_delete=models.CASCADE,
        related_name="access_rules",
        verbose_name="Бизнес-объект"
    )
    
    # Права на свои объекты (owner_id = current_user.id)
    read_permission = models.BooleanField(default=False, verbose_name="Чтение своих")
    create_permission = models.BooleanField(default=False, verbose_name="Создание своих")
    update_permission = models.BooleanField(default=False, verbose_name="Обновление своих")
    delete_permission = models.BooleanField(default=False, verbose_name="Удаление своих")
    
    # Права на все объекты
    read_all_permission = models.BooleanField(default=False, verbose_name="Чтение всех")
    update_all_permission = models.BooleanField(default=False, verbose_name="Обновление всех")
    delete_all_permission = models.BooleanField(default=False, verbose_name="Удаление всех")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Правило доступа"
        verbose_name_plural = "Правила доступа"
        unique_together = [["role", "element"]]
        ordering = ["role", "element"]

    def __str__(self):
        return f"{self.role.name} -> {self.element.code}"
