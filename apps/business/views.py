"""
Mock views для бизнес-объектов
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.authorization.permissions import HasElementPermission


# Mock данные
MOCK_PRODUCTS = [
    {"id": 1, "name": "Товар 1", "price": 100, "owner_id": None},
    {"id": 2, "name": "Товар 2", "price": 200, "owner_id": None},
    {"id": 3, "name": "Товар 3", "price": 300, "owner_id": None},
]

MOCK_ORDERS = [
    {"id": 1, "order_number": "ORD-001", "total": 500, "owner_id": None},
    {"id": 2, "order_number": "ORD-002", "total": 750, "owner_id": None},
    {"id": 3, "order_number": "ORD-003", "total": 1000, "owner_id": None},
]

MOCK_STORES = [
    {"id": 1, "name": "Магазин 1", "address": "Адрес 1", "owner_id": None},
    {"id": 2, "name": "Магазин 2", "address": "Адрес 2", "owner_id": None},
    {"id": 3, "name": "Магазин 3", "address": "Адрес 3", "owner_id": None},
]


class MockObject:
    """Mock объект для проверки прав доступа"""
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def products_list(request):
    """Список товаров"""
    if request.method == "GET":
        # Проверка прав на чтение
        permission = HasElementPermission("products", "read")
        if not permission.has_permission(request, None):
            return Response(
                {"error": "Нет доступа к товарам"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        # Фильтрация по владельцу, если нет прав на чтение всех
        rule = None
        if request.user.role:
            from apps.authorization.models import BusinessElement, AccessRoleRule
            try:
                element = BusinessElement.objects.get(code="products")
                rule = AccessRoleRule.objects.get(
                    role=request.user.role,
                    element=element
                )
            except:
                pass
        
        products = MOCK_PRODUCTS.copy()
        if rule and not rule.read_all_permission and rule.read_permission:
            # Показываем только свои товары
            products = [p for p in products if p.get("owner_id") == str(request.user.id)]
        
        return Response({"products": products})
    
    elif request.method == "POST":
        # Проверка прав на создание
        permission = HasElementPermission("products", "create")
        if not permission.has_permission(request, None):
            return Response(
                {"error": "Нет прав на создание товаров"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        new_product = {
            "id": len(MOCK_PRODUCTS) + 1,
            "name": request.data.get("name", "Новый товар"),
            "price": request.data.get("price", 0),
            "owner_id": str(request.user.id),
        }
        MOCK_PRODUCTS.append(new_product)
        return Response(new_product, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def product_detail(request, pk):
    """Детали товара"""
    try:
        product_data = next(p for p in MOCK_PRODUCTS if p["id"] == int(pk))
    except StopIteration:
        return Response(
            {"error": "Товар не найден"},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    product = MockObject(product_data)
    
    if request.method == "GET":
        permission = HasElementPermission("products", "read")
        if not permission.has_object_permission(request, None, product):
            return Response(
                {"error": "Нет доступа к этому товару"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(product_data)
    
    elif request.method == "PATCH":
        permission = HasElementPermission("products", "update")
        if not permission.has_object_permission(request, None, product):
            return Response(
                {"error": "Нет прав на обновление этого товара"},
                status=status.HTTP_403_FORBIDDEN,
            )
        product_data.update(request.data)
        return Response(product_data)
    
    elif request.method == "DELETE":
        permission = HasElementPermission("products", "delete")
        if not permission.has_object_permission(request, None, product):
            return Response(
                {"error": "Нет прав на удаление этого товара"},
                status=status.HTTP_403_FORBIDDEN,
            )
        MOCK_PRODUCTS.remove(product_data)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def orders_list(request):
    """Список заказов"""
    if request.method == "GET":
        permission = HasElementPermission("orders", "read")
        if not permission.has_permission(request, None):
            return Response(
                {"error": "Нет доступа к заказам"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        rule = None
        if request.user.role:
            from apps.authorization.models import BusinessElement, AccessRoleRule
            try:
                element = BusinessElement.objects.get(code="orders")
                rule = AccessRoleRule.objects.get(
                    role=request.user.role,
                    element=element
                )
            except:
                pass
        
        orders = MOCK_ORDERS.copy()
        if rule and not rule.read_all_permission and rule.read_permission:
            orders = [o for o in orders if o.get("owner_id") == str(request.user.id)]
        
        return Response({"orders": orders})
    
    elif request.method == "POST":
        permission = HasElementPermission("orders", "create")
        if not permission.has_permission(request, None):
            return Response(
                {"error": "Нет прав на создание заказов"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        new_order = {
            "id": len(MOCK_ORDERS) + 1,
            "order_number": f"ORD-{len(MOCK_ORDERS) + 1:03d}",
            "total": request.data.get("total", 0),
            "owner_id": str(request.user.id),
        }
        MOCK_ORDERS.append(new_order)
        return Response(new_order, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    """Детали заказа"""
    try:
        order_data = next(o for o in MOCK_ORDERS if o["id"] == int(pk))
    except StopIteration:
        return Response(
            {"error": "Заказ не найден"},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    order = MockObject(order_data)
    
    if request.method == "GET":
        permission = HasElementPermission("orders", "read")
        if not permission.has_object_permission(request, None, order):
            return Response(
                {"error": "Нет доступа к этому заказу"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(order_data)
    
    elif request.method == "PATCH":
        permission = HasElementPermission("orders", "update")
        if not permission.has_object_permission(request, None, order):
            return Response(
                {"error": "Нет прав на обновление этого заказа"},
                status=status.HTTP_403_FORBIDDEN,
            )
        order_data.update(request.data)
        return Response(order_data)
    
    elif request.method == "DELETE":
        permission = HasElementPermission("orders", "delete")
        if not permission.has_object_permission(request, None, order):
            return Response(
                {"error": "Нет прав на удаление этого заказа"},
                status=status.HTTP_403_FORBIDDEN,
            )
        MOCK_ORDERS.remove(order_data)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def stores_list(request):
    """Список магазинов"""
    if request.method == "GET":
        permission = HasElementPermission("stores", "read")
        if not permission.has_permission(request, None):
            return Response(
                {"error": "Нет доступа к магазинам"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        rule = None
        if request.user.role:
            from apps.authorization.models import BusinessElement, AccessRoleRule
            try:
                element = BusinessElement.objects.get(code="stores")
                rule = AccessRoleRule.objects.get(
                    role=request.user.role,
                    element=element
                )
            except:
                pass
        
        stores = MOCK_STORES.copy()
        if rule and not rule.read_all_permission and rule.read_permission:
            stores = [s for s in stores if s.get("owner_id") == str(request.user.id)]
        
        return Response({"stores": stores})
    
    elif request.method == "POST":
        permission = HasElementPermission("stores", "create")
        if not permission.has_permission(request, None):
            return Response(
                {"error": "Нет прав на создание магазинов"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        new_store = {
            "id": len(MOCK_STORES) + 1,
            "name": request.data.get("name", "Новый магазин"),
            "address": request.data.get("address", ""),
            "owner_id": str(request.user.id),
        }
        MOCK_STORES.append(new_store)
        return Response(new_store, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def store_detail(request, pk):
    """Детали магазина"""
    try:
        store_data = next(s for s in MOCK_STORES if s["id"] == int(pk))
    except StopIteration:
        return Response(
            {"error": "Магазин не найден"},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    store = MockObject(store_data)
    
    if request.method == "GET":
        permission = HasElementPermission("stores", "read")
        if not permission.has_object_permission(request, None, store):
            return Response(
                {"error": "Нет доступа к этому магазину"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(store_data)
    
    elif request.method == "PATCH":
        permission = HasElementPermission("stores", "update")
        if not permission.has_object_permission(request, None, store):
            return Response(
                {"error": "Нет прав на обновление этого магазина"},
                status=status.HTTP_403_FORBIDDEN,
            )
        store_data.update(request.data)
        return Response(store_data)
    
    elif request.method == "DELETE":
        permission = HasElementPermission("stores", "delete")
        if not permission.has_object_permission(request, None, store):
            return Response(
                {"error": "Нет прав на удаление этого магазина"},
                status=status.HTTP_403_FORBIDDEN,
            )
        MOCK_STORES.remove(store_data)
        return Response(status=status.HTTP_204_NO_CONTENT)
