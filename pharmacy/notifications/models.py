from django.db import models
from django.conf import settings


class Notification(models.Model):

    TYPE_CHOICES = [
        ("account", "حساب جديد"),
        ("approval", "موافقة"),
        ("rejection", "رفض"),
        ("order", "طلب"),
        ("stock", "المخزون"),
        ("purchase", "التوريد"),
        ("profile", "البيانات الشخصية"),
        ("password", "كلمة المرور"),
        ("system", "النظام"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="المستخدم"
    )

    title = models.CharField(
        max_length=200,
        verbose_name="عنوان الإشعار"
    )

    message = models.TextField(
        verbose_name="محتوى الإشعار"
    )

    notification_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="system",
        verbose_name="نوع الإشعار"
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name="تمت القراءة"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإشعار"
    )

    class Meta:
        verbose_name = "إشعار"
        verbose_name_plural = "الإشعارات"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title