from django.db import models


class ProductType(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="اسم نوع المنتج"
    )

    description = models.TextField(
        blank=True,
        verbose_name="الوصف"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "نوع المنتج"
        verbose_name_plural = "أنواع المنتجات"
        ordering = ["name"]