from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views
from accounts import views as account_views


urlpatterns = [

    # =========================================================
    # تسجيل الدخول
    # =========================================================

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    # =========================================================
    # لوحة التحكم
    # =========================================================

    path(
        "dashboard/",
        views.home,
        name="dashboard"
    ),

    # =========================================================
    # تسجيل الخروج
    # =========================================================

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    # =========================================================
    # صفحات النظام
    # =========================================================

    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "contact/",
        views.contact,
        name="contact"
    ),

    path(
        "forgot-password/",
        views.forgot_password,
        name="forgot_password"
    ),

    path(
        "forgot-password/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    path(
        "reset-password/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete")
        ),
        name="password_reset_confirm"
    ),

    path(
        "reset-password/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),

    path(
        "404/",
        views.page_not_found,
        name="page404"
    ),

    # =========================================================
    # إعدادات الحساب
    # تستخدم وظائف accounts
    # حتى تعمل لجميع المستخدمين مع الإشعارات
    # =========================================================

    path(
        "settings/",
        account_views.settings_view,
        name="settings"
    ),

    path(
        "change-password/",
        account_views.change_password,
        name="change_password"
    ),

]