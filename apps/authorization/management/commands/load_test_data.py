"""
Management команда для загрузки тестовых данных
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.authorization.models import Role, BusinessElement, AccessRoleRule

User = get_user_model()


class Command(BaseCommand):
    help = "Загрузка тестовых данных: роли, бизнес-объекты, правила доступа, пользователи"
    
    def handle(self, *args, **options):
        self.stdout.write("Создание ролей...")
        self.create_roles()
        
        self.stdout.write("Создание бизнес-объектов...")
        self.create_business_elements()
        
        self.stdout.write("Создание правил доступа...")
        self.create_access_rules()
        
        self.stdout.write("Создание тестовых пользователей...")
        self.create_test_users()
        
        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно загружены!"))
    
    def create_roles(self):
        """Создание ролей"""
        roles_data = [
            {"name": "admin", "description": "Администратор - полный доступ"},
            {"name": "manager", "description": "Менеджер - чтение всего, редактирование своего"},
            {"name": "user", "description": "Пользователь - CRUD только своих объектов"},
            {"name": "guest", "description": "Гость - только чтение публичных данных"},
        ]
        
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                name=role_data["name"],
                defaults={"description": role_data["description"]}
            )
            if created:
                self.stdout.write(f"  Создана роль: {role.name}")
            else:
                self.stdout.write(f"  Роль уже существует: {role.name}")
    
    def create_business_elements(self):
        """Создание бизнес-объектов"""
        elements_data = [
            {"code": "users", "name": "Пользователи", "description": "Управление пользователями"},
            {"code": "products", "name": "Товары", "description": "Управление товарами"},
            {"code": "orders", "name": "Заказы", "description": "Управление заказами"},
            {"code": "stores", "name": "Магазины", "description": "Управление магазинами"},
            {"code": "access_rules", "name": "Правила доступа", "description": "Управление правилами доступа"},
        ]
        
        for element_data in elements_data:
            element, created = BusinessElement.objects.get_or_create(
                code=element_data["code"],
                defaults={
                    "name": element_data["name"],
                    "description": element_data["description"]
                }
            )
            if created:
                self.stdout.write(f"  Создан объект: {element.code}")
            else:
                self.stdout.write(f"  Объект уже существует: {element.code}")
    
    def create_access_rules(self):
        """Создание правил доступа"""
        admin_role = Role.objects.get(name="admin")
        manager_role = Role.objects.get(name="manager")
        user_role = Role.objects.get(name="user")
        guest_role = Role.objects.get(name="guest")
        
        elements = {
            elem.code: elem for elem in BusinessElement.objects.all()
        }
        
        # Администратор - полный доступ ко всему
        for element in elements.values():
            AccessRoleRule.objects.get_or_create(
                role=admin_role,
                element=element,
                defaults={
                    "read_permission": True,
                    "read_all_permission": True,
                    "create_permission": True,
                    "update_permission": True,
                    "update_all_permission": True,
                    "delete_permission": True,
                    "delete_all_permission": True,
                }
            )
        
        # Менеджер - чтение всего, редактирование своего
        for element in elements.values():
            AccessRoleRule.objects.get_or_create(
                role=manager_role,
                element=element,
                defaults={
                    "read_permission": True,
                    "read_all_permission": True,
                    "create_permission": True,
                    "update_permission": True,
                    "update_all_permission": False,
                    "delete_permission": True,
                    "delete_all_permission": False,
                }
            )
        
        # Пользователь - CRUD только своих объектов
        for element in elements.values():
            AccessRoleRule.objects.get_or_create(
                role=user_role,
                element=element,
                defaults={
                    "read_permission": True,
                    "read_all_permission": False,
                    "create_permission": True,
                    "update_permission": True,
                    "update_all_permission": False,
                    "delete_permission": True,
                    "delete_all_permission": False,
                }
            )
        
        # Гость - только чтение публичных данных (read_permission = False, read_all_permission = True для некоторых)
        for element_code, element in elements.items():
            AccessRoleRule.objects.get_or_create(
                role=guest_role,
                element=element,
                defaults={
                    "read_permission": False,
                    "read_all_permission": element_code in ["products", "stores"],  # Только товары и магазины
                    "create_permission": False,
                    "update_permission": False,
                    "update_all_permission": False,
                    "delete_permission": False,
                    "delete_all_permission": False,
                }
            )
        
        self.stdout.write("  Правила доступа созданы")
    
    def create_test_users(self):
        """Создание тестовых пользователей"""
        admin_role = Role.objects.get(name="admin")
        manager_role = Role.objects.get(name="manager")
        user_role = Role.objects.get(name="user")
        
        users_data = [
            {
                "email": "admin@example.com",
                "password": "admin123",
                "first_name": "Админ",
                "last_name": "Админов",
                "role": admin_role,
            },
            {
                "email": "manager@example.com",
                "password": "manager123",
                "first_name": "Менеджер",
                "last_name": "Менеджеров",
                "role": manager_role,
            },
            {
                "email": "user@example.com",
                "password": "user123",
                "first_name": "Пользователь",
                "last_name": "Пользователев",
                "role": user_role,
            },
        ]
        
        for user_data in users_data:
            password = user_data.pop("password")
            user, created = User.objects.get_or_create(
                email=user_data["email"],
                defaults=user_data
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(f"  Создан пользователь: {user.email} (пароль: {password})")
            else:
                self.stdout.write(f"  Пользователь уже существует: {user.email}")


