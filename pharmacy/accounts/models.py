from django.db import models


class User(models.Model):

    ROLE_CHOICES = [
        ("admin", "مدير"),
        ("pharmacist", "صيدلي"),
    ]

    full_name = models.CharField(
        max_length=200,
        verbose_name="الاسم الكامل"
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="اسم المستخدم"
    )

    email = models.EmailField(
        unique=True,
        verbose_name="البريد الإلكتروني"
    )

    phone = models.CharField(
        max_length=20,
        verbose_name="رقم الهاتف"
    )

    password = models.CharField(
        max_length=128,
        verbose_name="كلمة المرور"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="pharmacist",
        verbose_name="الدور"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="الحالة"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث"
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "مستخدم"
        verbose_name_plural = "المستخدمون"
        ordering = ["full_name"]