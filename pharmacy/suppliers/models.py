from django.db import models
from accounts.models import User


class Supplier(models.Model):

    # حساب المستخدم المرتبط بالمورد
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="supplier_profile",
        verbose_name="حساب المستخدم"
    )

    # اسم المورد
    full_name = models.CharField(
        max_length=200,
        verbose_name="اسم المورد"
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

    # اسم الشركة
    company_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="اسم الشركة"
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
        verbose_name = "مورد"
        verbose_name_plural = "الموردون"
        ordering = ["full_name"]