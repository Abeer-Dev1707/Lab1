from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.product_type_list,
        name="product_type_list"
    ),

    path(
        "add/",
        views.product_type_create,
        name="product_type_create"
    ),

    path(
        "edit/<int:pk>/",
        views.product_type_update,
        name="product_type_update"
    ),

    path(
        "delete/<int:pk>/",
        views.product_type_delete,
        name="product_type_delete"
    ),

]