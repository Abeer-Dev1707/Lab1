from django.db import models
from categories.models import Category
from product_types.models import ProductType
from suppliers.models import Supplier


# =========================================================
# المادة الفعالة
# =========================================================

class ActiveIngredient(models.Model):

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="اسم المادة الفعالة"
    )

    description = models.TextField(
        blank=True,
        verbose_name="الوصف"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإضافة"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "مادة فعالة"
        verbose_name_plural = "المواد الفعالة"
        ordering = ["name"]


# =========================================================
# الدواء
# =========================================================

class Medicine(models.Model):

    STATUS_CHOICES = [
        ('available', 'متوفر'),
        ('unavailable', 'غير متوفر'),
    ]

    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name="medicines",
        verbose_name="نوع المنتج",
        null=True,
        blank=True
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        related_name="medicines",
        verbose_name="المورد",
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=200,
        verbose_name="اسم الدواء"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="medicines",
        verbose_name="الفئة"
    )

    # =====================================================
    # علاقة Many-to-Many
    # =====================================================

    active_ingredients = models.ManyToManyField(
        ActiveIngredient,
        related_name="medicines",
        blank=True,
        verbose_name="المواد الفعالة"
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

    dosage_form = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="الشكل الدوائي"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "دواء"
        verbose_name_plural = "الأدوية"
        ordering = ['name']