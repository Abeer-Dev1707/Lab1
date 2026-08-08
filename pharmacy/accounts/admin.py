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