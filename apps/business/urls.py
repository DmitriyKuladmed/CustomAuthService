"""
URLs для бизнес-объектов
"""
from django.urls import path
from apps.business import views

app_name = "business"

urlpatterns = [
    path("products/", views.products_list, name="products-list"),
    path("products/<int:pk>/", views.product_detail, name="product-detail"),
    path("orders/", views.orders_list, name="orders-list"),
    path("orders/<int:pk>/", views.order_detail, name="order-detail"),
    path("stores/", views.stores_list, name="stores-list"),
    path("stores/<int:pk>/", views.store_detail, name="store-detail"),
]


