from django import forms
from django.forms import inlineformset_factory

from .models import Sale, SaleItem


# =========================================================
# نموذج فاتورة البيع
# =========================================================

class SaleForm(forms.ModelForm):

    class Meta:

        model = Sale

        fields = [
            "customer",
            "notes",
        ]

        labels = {
            "customer": "العميل",
            "notes": "ملاحظات",
        }

        widgets = {

            "customer": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "أضف ملاحظات إن وجدت..."
                }
            ),
        }


# =========================================================
# نموذج تفاصيل البيع
# =========================================================

class SaleItemForm(forms.ModelForm):

    class Meta:

        model = SaleItem

        fields = [
            "medicine",
            "quantity",
            "selling_price",
        ]

        labels = {
            "medicine": "الدواء",
            "quantity": "الكمية",
            "selling_price": "سعر البيع",
        }

        widgets = {

            "medicine": forms.Select(
                attrs={
                    "class": "form-select medicine-select"
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control quantity-input",
                    "min": 1
                }
            ),

            "selling_price": forms.NumberInput(
                attrs={
                    "class": "form-control selling-price-input",
                    "step": "0.01",
                    "min": "0"
                }
            ),
        }

    def clean_quantity(self):

        quantity = self.cleaned_data.get("quantity")

        if quantity is not None and quantity <= 0:

            raise forms.ValidationError(
                "يجب أن تكون الكمية أكبر من صفر."
            )

        return quantity

    def clean_selling_price(self):

        price = self.cleaned_data.get("selling_price")

        if price is not None and price < 0:

            raise forms.ValidationError(
                "لا يمكن أن يكون سعر البيع سالبًا."
            )

        return price


# =========================================================
# Formset لإضافة عدة منتجات داخل الفاتورة
# =========================================================

SaleItemFormSet = inlineformset_factory(

    Sale,
    SaleItem,

    form=SaleItemForm,

    extra=1,

    can_delete=True
)