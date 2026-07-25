from django.db import models
from suppliers.models import Supplier


class Medicine(models.Model):
    name = models.CharField(max_length=200, verbose_name="اسم الدواء")
    barcode = models.CharField(max_length=50, unique=True, verbose_name="الباركود")
    manufacturer = models.CharField(max_length=200, verbose_name="الشركة المصنعة")

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        verbose_name="المورد"
    )

    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="سعر الشراء")
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="سعر البيع")
    quantity = models.PositiveIntegerField(default=0, verbose_name="الكمية")
    expiry_date = models.DateField(verbose_name="تاريخ الانتهاء")

    def __str__(self):
        return self.name