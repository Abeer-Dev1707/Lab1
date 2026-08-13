from django import forms
from .models import Medicine


class MedicineForm(forms.ModelForm):

    class Meta:

        model = Medicine

        fields = [
            'name',
            "product_type",
            'supplier',
            'category',
            "dosage_form",
            'barcode',
            'manufacturer',
            'purchase_price',
            'selling_price',
            'quantity',
            'minimum_stock',
            'production_date',
            'expiry_date',
            'description',
        ]

        labels = {
            'name': 'اسم الدواء',
            'product_type': 'نوع المنتج',
            'supplier': 'المورد',
            'category': 'الفئة',
            'barcode': 'الباركود',
            'manufacturer': 'الشركة المصنعة',
            'purchase_price': 'سعر الشراء',
            'selling_price': 'سعر البيع',
            'quantity': 'الكمية',
            'minimum_stock': 'الحد الأدنى للمخزون',
            'production_date': 'تاريخ الإنتاج',
            'expiry_date': 'تاريخ الانتهاء',
            'description': 'الوصف',
            "dosage_form": "الشكل الدوائي",
        }

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'product_type': forms.Select(attrs={
                'class': 'form-select'
            }),

            'supplier': forms.Select(attrs={
                'class': 'form-select'
            }),

            'category': forms.Select(attrs={
                'class': 'form-select'
            }),

            'barcode': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'manufacturer': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'purchase_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),

            'selling_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'minimum_stock': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'production_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),

            "dosage_form": forms.TextInput(attrs={
                "class": "form-control"
            }),
        }