from django.urls import path
from . import views


urlpatterns = [

    # ==========================================
    # إدارة المستخدمين - المدير
    # ==========================================

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


    # ==========================================
    # التسجيل العام
    # ==========================================

    path(
        "register/",
        views.register,
        name="register"
    ),


    # ==========================================
    # طلبات إنشاء الحسابات - المدير
    # ==========================================

    path(
        "requests/",
        views.account_requests,
        name="account_requests"
    ),


    # ==========================================
    # الموافقة على الحساب
    # ==========================================

    path(
        "requests/approve/<int:pk>/",
        views.approve_account,
        name="approve_account"
    ),


    # ==========================================
    # رفض الحساب
    # ==========================================

    path(
        "requests/reject/<int:pk>/",
        views.reject_account,
        name="reject_account"
    ),

]