from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # الأدوية
    # =====================================================

    path(
        "",
        views.medicine_list,
        name="medicine_list"
    ),

    path(
        "add/",
        views.medicine_create,
        name="medicine_create"
    ),

    path(
        "edit/<int:pk>/",
        views.medicine_update,
        name="medicine_update"
    ),

    path(
        "delete/<int:pk>/",
        views.medicine_delete,
        name="medicine_delete"
    ),


    # =====================================================
    # منتجات المورد
    # =====================================================

    path(
        "my-products/",
        views.supplier_medicines,
        name="supplier_medicines"
    ),


    # =====================================================
    # الطرق الثلاث لكتابة Forms
    # =====================================================

    # الطريقة الأولى:
    # HTML Form عادي
    path(
        "simple-form/",
        views.simple_html_form,
        name="simple_html_form"
    ),

    # الطريقة الثانية:
    # Django forms.Form
    path(
        "django-form/",
        views.django_form,
        name="django_form"
    ),

    # الطريقة الثالثة:
    # Django ModelForm
    # موجودة أصلًا من خلال:
    # add/ و edit/
]