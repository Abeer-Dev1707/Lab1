from django.urls import path
from . import views

urlpatterns = [
    path("", views.medicine_list, name="medicine_list"),
    path("add/", views.medicine_create, name="medicine_create"),
    path("edit/<int:pk>/", views.medicine_update, name="medicine_update"),
    path("delete/<int:pk>/", views.medicine_delete, name="medicine_delete"),
]