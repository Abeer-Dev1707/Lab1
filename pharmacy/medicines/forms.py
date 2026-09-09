from django import forms

from .models import Medicine, ActiveIngredient


# =========================================================
# البحث عن دواء
# باستخدام forms.Form
# =========================================================

class SearchMedicineForm(forms.Form):

    search = forms.CharField(
        max_length=200,
        required=False,
        label="البحث عن دواء",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "اكتب اسم الدواء أو الباركود..."
            }
        )
    )


# =========================================================
# إضافة وتعديل الدواء
# باستخدام forms.ModelForm
# =========================================================

class MedicineForm(forms.ModelForm):

    class Meta:

        model = Medicine

        fields = [
            "name",
            "product_type",
            "supplier",
            "category",
            "active_ingredients",
            "dosage_form",
            "barcode",
            "manufacturer",
            "purchase_price",
            "selling_price",
            "quantity",
            "minimum_stock",
            "production_date",
            "expiry_date",
            "description",
        ]

        labels = {

            "name": "اسم الدواء",

            "product_type": "نوع المنتج",

            "supplier": "المورد",

            "category": "الفئة",

            "active_ingredients": "المواد الفعالة",

            "dosage_form": "الشكل الدوائي",

            "barcode": "الباركود",

            "manufacturer": "الشركة المصنعة",

            "purchase_price": "سعر الشراء",

            "selling_price": "سعر البيع",

            "quantity": "الكمية",

            "minimum_stock": "الحد الأدنى للمخزون",

            "production_date": "تاريخ الإنتاج",

            "expiry_date": "تاريخ الانتهاء",

            "description": "الوصف",
        }

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "أدخل اسم الدواء"
                }
            ),

            "product_type": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "supplier": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            # =================================================
            # المواد الفعالة
            # يسمح باختيار أكثر من مادة
            # =================================================

            "active_ingredients": forms.SelectMultiple(
                attrs={
                    "class": "form-select",
                    "size": "5"
                }
            ),

            "dosage_form": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "مثال: أقراص، شراب، كبسولات..."
                }
            ),

            "barcode": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "أدخل الباركود"
                }
            ),

            "manufacturer": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "اسم الشركة المصنعة"
                }
            ),

            "purchase_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "selling_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0"
                }
            ),

            "minimum_stock": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0"
                }
            ),

            "production_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "expiry_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "وصف الدواء..."
                }
            ),
        }