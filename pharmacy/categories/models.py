from django.db import models


class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="اسم الفئة"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="الوصف"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث"
    )

    class Meta:
        verbose_name = "فئة"
        verbose_name_plural = "الفئات"
        ordering = ["name"]

    def __str__(self):
        return self.name