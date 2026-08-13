from django.urls import path

from . import views


urlpatterns = [

    # قائمة المخزون
    path(
        "",
        views.inventory_list,
        name="inventory_list"
    ),

    # تفاصيل الدواء
    path(
        "detail/<int:pk>/",
        views.inventory_detail,
        name="inventory_detail"
    ),

    # إضافة دواء
    path(
        "create/",
        views.inventory_create,
        name="inventory_create"
    ),

    # تعديل دواء
    path(
        "update/<int:pk>/",
        views.inventory_update,
        name="inventory_update"
    ),

]