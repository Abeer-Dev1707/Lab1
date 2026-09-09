from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "username",
        "email",
        "phone",
        "role",
        "is_active",
        "created_at",
    )

    list_filter = (
        "role",
        "is_active",
        "created_at",
    )

    search_fields = (
        "full_name",
        "username",
        "email",
        "phone",
    )

    ordering = (
        "full_name",
    )

# =========================================================
# حماية Django Admin
# المستخدم الوحيد المسموح له بالدخول هو Abeer_Ahmed
# =========================================================

_original_admin_has_permission = admin.site.has_permission


def pharmacy_admin_has_permission(request):

    user = request.user

    return bool(
        user.is_authenticated
        and user.is_active
        and user.username == "Abeer_Ahmed"
        and user.is_staff
        and user.is_superuser
    )


admin.site.has_permission = pharmacy_admin_has_permission


# هوية لوحة الإدارة بما يتوافق مع اسم المشروع.
admin.site.site_header = "إدارة صيدلية الحياة"
admin.site.site_title = "إدارة صيدلية الحياة"
admin.site.index_title = "لوحة إدارة صيدلية الحياة"
