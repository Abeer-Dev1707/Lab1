from django.urls import path
from . import views


urlpatterns = [

    # قائمة طلبات التوريد
    path(
        "",
        views.purchase_list,
        name="purchase_list"
    ),

    # إنشاء طلب توريد
    path(
        "add/",
        views.purchase_create,
        name="purchase_create"
    ),

    # تفاصيل طلب التوريد
    path(
        "details/<int:pk>/",
        views.purchase_detail,
        name="purchase_detail"
    ),

    # طلبات التوريد للمورد
    path(
        "my-orders/",
        views.supplier_orders,
        name="supplier_orders"
    ),

     # موافقة المورد
    path(
        "supplier/approve/<int:pk>/",
        views.supplier_approve_order,
        name="supplier_approve_order"
    ),

    # رفض المورد
    path(
        "supplier/reject/<int:pk>/",
        views.supplier_reject_order,
        name="supplier_reject_order"
    ),

       # تأكيد استلام التوريد
    path(
        "receive/<int:pk>/",
        views.purchase_receive,
        name="purchase_receive"
    ),

    path(
    "receive/<int:pk>/",
    views.purchase_receive,
    name="purchase_receive"
),

]