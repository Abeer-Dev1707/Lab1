from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.user_list,
        name="user_list"
    ),

    path(
        "add/",
        views.user_create,
        name="user_create"
    ),

    path(
        "edit/<int:pk>/",
        views.user_update,
        name="user_update"
    ),

    path(
        "delete/<int:pk>/",
        views.user_delete,
        name="user_delete"
    ),

]