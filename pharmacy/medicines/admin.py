from django.contrib import admin
from .models import Medicine


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'manufacturer',
        'selling_price',
        'quantity',
        'status',
        'expiry_date',
    )

    list_filter = (
        'category',
        'status',
        'manufacturer',
    )

    search_fields = (
        'name',
        'barcode',
        'manufacturer',
    )

    ordering = ('name',)