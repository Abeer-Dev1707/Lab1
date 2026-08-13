"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [

    # =========================================================
    # الصفحة الرئيسية
    # تحويل / إلى صفحة تسجيل الدخول
    # =========================================================

    path(
        "",
        RedirectView.as_view(
            pattern_name="login",
            permanent=False
        )
    ),


    # =========================================================
    # Django Admin
    # =========================================================

    path(
        "admin/",
        admin.site.urls
    ),


    # =========================================================
    # Dashboard
    # =========================================================

    path(
        "dashboard/",
        include("dashboard.urls")
    ),


    # =========================================================
    # Categories
    # =========================================================

    path(
        "categories/",
        include("categories.urls")
    ),


    # =========================================================
    # Medicines
    # =========================================================

    path(
        "medicines/",
        include("medicines.urls")
    ),


    # =========================================================
    # Users / Accounts
    # =========================================================

    path(
        "users/",
        include("accounts.urls")
    ),


    # =========================================================
    # Product Types
    # =========================================================

    path(
        "product-types/",
        include("product_types.urls")
    ),


    # =========================================================
    # Customers
    # =========================================================

    path(
        "customers/",
        include("customers.urls")
    ),


    # =========================================================
    # Suppliers
    # =========================================================

    path(
        "suppliers/",
        include("suppliers.urls")
    ),


    # =========================================================
    # Purchases / Supplier Orders
    # =========================================================

    path(
        "purchases/",
        include("purchases.urls")
    ),


    # =========================================================
    # Sales
    # =========================================================

    path(
        "sales/",
        include("sales.urls")
    ),


    # =========================================================
    # Inventory
    # =========================================================

    path(
        "inventory/",
        include("inventory.urls")
    ),

]