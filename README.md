# CustomAuthService

Кастомная система аутентификации и авторизации на Django REST Framework с JWT токенами и RBAC (Role-Based Access Control).

## Описание

Система реализует:
- Кастомную аутентификацию через JWT токены (без использования встроенных возможностей Django)
- Систему разграничения прав доступа (RBAC) с гибкой настройкой правил
- Управление пользователями с мягким удалением
- API для управления ролями и правилами доступа (для администраторов)
- Mock бизнес-объекты для демонстрации работы системы доступа

## Технологии

- Django 4.2+
- Django REST Framework 3.14+
- PostgreSQL
- JWT (PyJWT)
- bcrypt для хеширования паролей
- Pydantic Settings для управления переменными окружения

## Установка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd CustomAuthService
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных

Создайте базу данных PostgreSQL:

```sql
CREATE DATABASE customauth;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE customauth TO postgres;
```

### 5. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
# Django Settings
SECRET_KEY=django-insecure-zt14damxagbm+(l&q4d=0b)&3rwh_6)gv)54sw3n5e2_h^iau3
DEBUG=True
ALLOWED_HOSTS=

# Database Settings
DB_NAME=customauth
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# JWT Settings
JWT_SECRET_KEY=jwt-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 6. Применение миграций

```bash
python manage.py migrate
```

### 7. Загрузка тестовых данных

```bash
python manage.py load_test_data
```

### 8. Запуск сервера

```bash
python manage.py runserver
```

## Схема базы данных

### Таблицы

#### users
- `id` (UUID, PK) - Уникальный идентификатор
- `email` (Email, UK) - Email пользователя
- `password` (CharField) - Хеш пароля (bcrypt)
- `first_name` (CharField) - Имя
- `last_name` (CharField) - Фамилия
- `patronymic` (CharField) - Отчество
- `role_id` (FK -> roles) - Роль пользователя
- `is_active` (Boolean) - Активен ли пользователь (для мягкого удаления)
- `created_at` (DateTime) - Дата создания
- `updated_at` (DateTime) - Дата обновления

#### roles
- `id` (Integer, PK) - Уникальный идентификатор
- `name` (CharField, UK) - Название роли
- `description` (TextField) - Описание роли
- `created_at` (DateTime) - Дата создания
- `updated_at` (DateTime) - Дата обновления

#### business_elements
- `id` (Integer, PK) - Уникальный идентификатор
- `code` (CharField, UK) - Код объекта (например, "products", "orders")
- `name` (CharField) - Название объекта
- `description` (TextField) - Описание объекта
- `created_at` (DateTime) - Дата создания
- `updated_at` (DateTime) - Дата обновления

#### access_roles_rules
- `id` (Integer, PK) - Уникальный идентификатор
- `role_id` (FK -> roles) - Роль
- `element_id` (FK -> business_elements) - Бизнес-объект
- `read_permission` (Boolean) - Чтение своих объектов
- `read_all_permission` (Boolean) - Чтение всех объектов
- `create_permission` (Boolean) - Создание своих объектов
- `update_permission` (Boolean) - Обновление своих объектов
- `update_all_permission` (Boolean) - Обновление всех объектов
- `delete_permission` (Boolean) - Удаление своих объектов
- `delete_all_permission` (Boolean) - Удаление всех объектов
- `created_at` (DateTime) - Дата создания
- `updated_at` (DateTime) - Дата обновления

### Логика разрешений

- `*_permission` - действие над своими объектами (где `owner_id = current_user.id`)
- `*_all_permission` - действие над всеми объектами

## API Endpoints

### Аутентификация

#### POST `/api/auth/register/`
Регистрация нового пользователя.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "password_confirm": "password123",
  "first_name": "Иван",
  "last_name": "Иванов",
  "patronymic": "Иванович"
}
```

**Response:**
```json
{
  "message": "Пользователь успешно зарегистрирован",
  "access_token": "...",
  "refresh_token": "...",
  "user": {
    "id": "...",
    "email": "user@example.com",
    "first_name": "Иван",
    "last_name": "Иванов"
  }
}
```

#### POST `/api/auth/login/`
Вход в систему.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "message": "Успешный вход в систему",
  "access_token": "...",
  "refresh_token": "...",
  "user": {...}
}
```

#### POST `/api/auth/logout/`
Выход из системы (требует аутентификации).

**Headers:**
```
Authorization: Bearer <access_token>
```

#### POST `/api/auth/refresh/`
Обновление access токена.

**Request:**
```json
{
  "refresh_token": "..."
}
```

**Response:**
```json
{
  "access_token": "..."
}
```

### Пользователи

#### GET `/api/users/me/`
Получение профиля текущего пользователя.

**Headers:**
```
Authorization: Bearer <access_token>
```

#### PATCH `/api/users/me/`
Обновление профиля текущего пользователя.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "first_name": "Новое имя",
  "last_name": "Новая фамилия"
}
```

#### DELETE `/api/users/me/`
Мягкое удаление аккаунта (устанавливает `is_active=False`).

**Headers:**
```
Authorization: Bearer <access_token>
```

#### GET `/api/users/`
Список пользователей (только для администратора).

**Headers:**
```
Authorization: Bearer <access_token>
```

#### GET `/api/users/{id}/`
Детали пользователя (только для администратора).

### Административные API (только для администраторов)

#### GET `/api/admin/roles/`
Список ролей.

#### POST `/api/admin/roles/`
Создание новой роли.

#### GET `/api/admin/elements/`
Список бизнес-объектов.

#### GET `/api/admin/rules/`
Список правил доступа.

**Query параметры:**
- `role_id` - фильтрация по роли
- `element_id` - фильтрация по элементу

#### POST `/api/admin/rules/`
Создание нового правила доступа.

**Request:**
```json
{
  "role": 1,
  "element": 2,
  "read_permission": true,
  "read_all_permission": false,
  "create_permission": true,
  "update_permission": true,
  "update_all_permission": false,
  "delete_permission": true,
  "delete_all_permission": false
}
```

#### PATCH `/api/admin/rules/{id}/`
Изменение правила доступа.

#### DELETE `/api/admin/rules/{id}/`
Удаление правила доступа.

#### PATCH `/api/admin/users/{id}/assign_role/`
Назначение роли пользователю.

**Request:**
```json
{
  "role_id": 1
}
```

### Бизнес-объекты (Mock)

#### GET `/api/products/`
Список товаров.

#### POST `/api/products/`
Создание товара.

#### GET `/api/products/{id}/`
Детали товара.

#### PATCH `/api/products/{id}/`
Обновление товара.

#### DELETE `/api/products/{id}/`
Удаление товара.

Аналогичные endpoints для:
- `/api/orders/` - заказы
- `/api/stores/` - магазины

## Тестовые данные

После выполнения `python manage.py load_test_data` создаются:

### Роли:
- **admin** - полный доступ ко всем ресурсам
- **manager** - чтение всего, редактирование своего
- **user** - CRUD только своих объектов
- **guest** - только чтение публичных данных

### Пользователи:
- `admin@example.com` / `admin123` (роль: admin)
- `manager@example.com` / `manager123` (роль: manager)
- `user@example.com` / `user123` (роль: user)

### Бизнес-объекты:
- users - Пользователи
- products - Товары
- orders - Заказы
- stores - Магазины
- access_rules - Правила доступа

## Примеры использования

### 1. Регистрация и вход

```bash
# Регистрация
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "password_confirm": "test123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Вход
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
```

### 2. Получение профиля

```bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer <access_token>"
```

### 3. Работа с товарами

```bash
# Список товаров
curl -X GET http://localhost:8000/api/products/ \
  -H "Authorization: Bearer <access_token>"

# Создание товара
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Новый товар",
    "price": 1000
  }'
```

## Обработка ошибок

- **401 Unauthorized** - Пользователь не аутентифицирован или токен недействителен
- **403 Forbidden** - Пользователь аутентифицирован, но не имеет прав доступа к ресурсу
- **404 Not Found** - Ресурс не найден
- **400 Bad Request** - Неверные данные запроса

## Структура проекта

```
CustomAuthService/
├── config/                    # Настройки Django проекта
│   ├── settings.py
│   ├── urls.py
│   ├── env_settings.py        # Pydantic settings
│   └── wsgi.py
├── apps/
│   ├── users/                 # Модуль пользователей
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── authentication/        # Модуль аутентификации
│   │   ├── middleware.py
│   │   ├── utils.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── authorization/         # Модуль авторизации (RBAC)
│   │   ├── models.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── management/commands/
│   │       └── load_test_data.py
│   └── business/              # Mock бизнес-объекты
│       ├── views.py
│       └── urls.py
├── requirements.txt
├── manage.py
└── README.md
```

## Особенности реализации

1. **Кастомная аутентификация**: Используется JWT без стандартных механизмов Django
2. **Хеширование паролей**: bcrypt вместо встроенного хеширования Django
3. **Middleware**: Кастомный middleware для установки `request.user` из JWT токена
4. **RBAC**: Гибкая система прав с разделением на действия над своими и всеми объектами
5. **Мягкое удаление**: Пользователи не удаляются физически, а помечаются как неактивные

## Лицензия

См. файл LICENSE
