from django.db import models

from suppliers.models import Supplier
from medicines.models import Medicine


# =========================================================
# طلب التوريد
# =========================================================

class PurchaseOrder(models.Model):

    STATUS_CHOICES = [
        ("pending", "قيد المراجعة"),
        ("approved", "تمت الموافقة"),
        ("rejected", "مرفوض"),
        ("completed", "مكتمل"),
    ]

    # -----------------------------------------------------
    # المورد
    # -----------------------------------------------------

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="purchase_orders",
        verbose_name="المورد"
    )

    # -----------------------------------------------------
    # حالة الطلب
    # -----------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="حالة الطلب"
    )

    # -----------------------------------------------------
    # ملاحظات
    # -----------------------------------------------------

    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات"
    )

    # -----------------------------------------------------
    # تاريخ إنشاء الطلب
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الطلب"
    )

    # -----------------------------------------------------
    # آخر تحديث
    # -----------------------------------------------------

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث"
    )

    def __str__(self):

        return f"طلب توريد #{self.id}"

    class Meta:

        verbose_name = "طلب توريد"
        verbose_name_plural = "طلبات التوريد"

        ordering = ["-created_at"]


# =========================================================
# تفاصيل طلب التوريد
# =========================================================

class PurchaseItem(models.Model):

    # -----------------------------------------------------
    # طلب التوريد
    # -----------------------------------------------------

    order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="طلب التوريد"
    )

    # -----------------------------------------------------
    # الدواء
    # -----------------------------------------------------

    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name="purchase_items",
        verbose_name="الدواء"
    )

    # -----------------------------------------------------
    # الكمية المطلوبة
    # -----------------------------------------------------

    quantity = models.PositiveIntegerField(
        verbose_name="الكمية المطلوبة"
    )

    # -----------------------------------------------------
    # سعر الشراء
    #
    # يكون فارغًا عند إنشاء الطلب من الصيدلية.
    # المورد هو الذي يحدد السعر لاحقًا.
    # -----------------------------------------------------

    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="سعر الشراء"
    )

    def __str__(self):

        return f"{self.medicine.name} - {self.quantity}"

    class Meta:

        verbose_name = "تفاصيل طلب التوريد"
        verbose_name_plural = "تفاصيل طلبات التوريد"