from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم المورد")
    phone = models.CharField(max_length=20, blank=True, verbose_name="رقم الهاتف")
    address = models.TextField(blank=True, verbose_name="العنوان")

    def __str__(self):
        return self.name