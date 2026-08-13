from django.db import models
from accounts.models import User


class Customer(models.Model):

    # حساب المستخدم المرتبط بالعميل
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="customer_profile",
        verbose_name="حساب المستخدم"
    )

    # الاسم الكامل
    full_name = models.CharField(
        max_length=200,
        verbose_name="الاسم الكامل"
    )

    # رقم الهاتف
    phone = models.CharField(
        max_length=20,
        verbose_name="رقم الهاتف"
    )

    # البريد الإلكتروني
    email = models.EmailField(
        blank=True,
        verbose_name="البريد الإلكتروني"
    )

    # العنوان
    address = models.TextField(
        blank=True,
        verbose_name="العنوان"
    )

    # ملاحظات
    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات"
    )

    # تاريخ الإضافة
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإضافة"
    )

    # آخر تحديث
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث"
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "عميل"
        verbose_name_plural = "العملاء"
        ordering = ["full_name"]

# =========================================================
# طلبات العملاء
# =========================================================

class CustomerOrder(models.Model):

    STATUS_CHOICES = [
        ("pending", "قيد المراجعة"),
        ("approved", "تمت الموافقة"),
        ("rejected", "مرفوض"),
        ("completed", "مكتمل"),
        ("cancelled", "ملغي"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="العميل"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="حالة الطلب"
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="الإجمالي"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الطلب"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث"
    )

    def __str__(self):
        return f"طلب العميل #{self.id}"

    class Meta:
        verbose_name = "طلب عميل"
        verbose_name_plural = "طلبات العملاء"
        ordering = ["-created_at"]


# =========================================================
# منتجات طلب العميل
# =========================================================

class CustomerOrderItem(models.Model):

    order = models.ForeignKey(
        CustomerOrder,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="الطلب"
    )

    medicine = models.ForeignKey(
        "medicines.Medicine",
        on_delete=models.PROTECT,
        related_name="customer_order_items",
        verbose_name="الدواء"
    )

    quantity = models.PositiveIntegerField(
        verbose_name="الكمية"
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="سعر البيع"
    )

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
            f"{self.medicine.name} - "
            f"{self.quantity}"
        )

    class Meta:
        verbose_name = "منتج في طلب العميل"
        verbose_name_plural = "منتجات طلبات العملاء"