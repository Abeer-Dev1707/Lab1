from django.db import models
from django.conf import settings

from customers.models import Customer


# =========================================================
# فاتورة البيع
# =========================================================

class Sale(models.Model):

    STATUS_CHOICES = [
        ("completed", "مكتملة"),
        ("cancelled", "ملغاة"),
    ]

    # -----------------------------------------------------
    # العميل
    # -----------------------------------------------------

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales",
        verbose_name="العميل"
    )

    # -----------------------------------------------------
    # طلب العميل المرتبط بالفاتورة
    # -----------------------------------------------------

    customer_order = models.OneToOneField(
        "customers.CustomerOrder",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sale",
        verbose_name="طلب العميل"
    )

    # -----------------------------------------------------
    # الموظف الذي قام بالبيع
    # -----------------------------------------------------

    cashier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales_made",
        verbose_name="موظف البيع"
    )

    # -----------------------------------------------------
    # حالة الفاتورة
    # -----------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="completed",
        verbose_name="حالة الفاتورة"
    )

    # -----------------------------------------------------
    # المجموع الكلي
    # -----------------------------------------------------

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="الإجمالي"
    )

    # -----------------------------------------------------
    # ملاحظات
    # -----------------------------------------------------

    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات"
    )

    # -----------------------------------------------------
    # التواريخ
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ البيع"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث"
    )

    def __str__(self):

        return f"فاتورة بيع #{self.id}"

    class Meta:

        verbose_name = "فاتورة بيع"
        verbose_name_plural = "فواتير البيع"

        ordering = ["-created_at"]


# =========================================================
# تفاصيل الفاتورة
# =========================================================

class SaleItem(models.Model):

    # -----------------------------------------------------
    # الفاتورة
    # -----------------------------------------------------

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="الفاتورة"
    )

    # -----------------------------------------------------
    # الدواء
    # -----------------------------------------------------

    medicine = models.ForeignKey(
        "medicines.Medicine",
        on_delete=models.PROTECT,
        related_name="sale_items",
        verbose_name="الدواء"
    )

    # -----------------------------------------------------
    # الكمية
    # -----------------------------------------------------

    quantity = models.PositiveIntegerField(
        verbose_name="الكمية"
    )

    # -----------------------------------------------------
    # سعر البيع وقت إجراء العملية
    # -----------------------------------------------------

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="سعر البيع"
    )

    # -----------------------------------------------------
    # الإجمالي للمنتج
    # -----------------------------------------------------

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="الإجمالي"
    )

    def save(self, *args, **kwargs):

        self.subtotal = (
            self.quantity * self.selling_price
        )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.medicine.name} "
            f"- {self.quantity}"
        )

    class Meta:

        verbose_name = "تفاصيل البيع"
        verbose_name_plural = "تفاصيل المبيعات"

        ordering = ["id"]