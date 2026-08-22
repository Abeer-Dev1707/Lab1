from django import forms
from django.forms import inlineformset_factory

from .models import PurchaseOrder, PurchaseItem


# =========================================================
# نموذج طلب التوريد
# =========================================================

class PurchaseOrderForm(forms.ModelForm):

    class Meta:

        model = PurchaseOrder

        fields = [
            "supplier",
            "notes",
        ]

        labels = {
            "supplier": "المورد",
            "notes": "ملاحظات",
        }

        widgets = {

            "supplier": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "أدخل ملاحظات الطلب إن وجدت",
                }
            ),
        }


# =========================================================
# نموذج المنتج داخل طلب التوريد
#
# الصيدلية تحدد:
#   - الدواء
#   - الكمية
#
# أما سعر الشراء فيحدده المورد لاحقًا.
# =========================================================

class PurchaseItemForm(forms.ModelForm):

    class Meta:

        model = PurchaseItem

        fields = [
            "medicine",
            "quantity",
        ]

        labels = {
            "medicine": "الدواء",
            "quantity": "الكمية المطلوبة",
        }

        widgets = {

            "medicine": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
        }


# =========================================================
# Formset لإضافة عدة أدوية إلى طلب واحد
# =========================================================

PurchaseItemFormSet = inlineformset_factory(

    PurchaseOrder,

    PurchaseItem,

    form=PurchaseItemForm,

    extra=1,

    can_delete=True,
)