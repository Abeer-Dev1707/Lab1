from django.db import models
from categories.models import Category


class Medicine(models.Model):

    STATUS_CHOICES = [
        ('available', 'متوفر'),
        ('unavailable', 'غير متوفر'),
    ]

    name = models.CharField(max_length=200, verbose_name="اسم الدواء")

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="medicines",
        verbose_name="الفئة"
    )

    barcode = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="الباركود"
    )

    manufacturer = models.CharField(
        max_length=200,
        verbose_name="الشركة المصنعة"
    )

    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="سعر الشراء"
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="سعر البيع"
    )

    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="الكمية"
    )

    minimum_stock = models.PositiveIntegerField(
        default=5,
        verbose_name="الحد الأدنى للمخزون"
    )

    production_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاريخ الإنتاج"
    )

    expiry_date = models.DateField(
        verbose_name="تاريخ الانتهاء"
    )

    description = models.TextField(
        blank=True,
        verbose_name="الوصف"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name="الحالة"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "دواء"
        verbose_name_plural = "الأدوية"
        ordering = ['name']