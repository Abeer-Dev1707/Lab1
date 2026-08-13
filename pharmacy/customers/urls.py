from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.customer_list,
        name="customer_list"
    ),

    path(
        "add/",
        views.customer_create,
        name="customer_create"
    ),

    path(
        "edit/<int:pk>/",
        views.customer_update,
        name="customer_update"
    ),

    path(
        "delete/<int:pk>/",
        views.customer_delete,
        name="customer_delete"
    ),

    path(
    "products/",
    views.customer_products,
    name="customer_products"
),

path(
    "orders/create/",
    views.customer_order_create,
    name="customer_order_create"
),

path(
    "orders/<int:pk>/",
    views.customer_order_detail,
    name="customer_order_detail"
),

path(
    "orders/",
    views.customer_orders,
    name="customer_orders"
),

 # =====================================================
    # إدارة طلبات العملاء
    # المدير + الصيدلي
    # =====================================================

    path(
        "orders/manage/",
        views.customer_order_manage,
        name="customer_order_manage"
    ),

    path(
    "orders/manage/<int:pk>/",
    views.customer_order_manage_detail,
    name="customer_order_manage_detail"
),

path(
    "orders/manage/<int:pk>/approve/",
    views.customer_order_approve,
    name="customer_order_approve"
),

path(
    "orders/manage/<int:pk>/reject/",
    views.customer_order_reject,
    name="customer_order_reject"
),

path(
    "invoice/<int:pk>/",
    views.customer_sale_detail,
    name="customer_sale_detail"
),

]