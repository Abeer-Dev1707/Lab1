from django import forms
from django.forms import inlineformset_factory

from .models import (
    Customer,
    CustomerOrder,
    CustomerOrderItem,
)

from medicines.models import Medicine
from accounts.validators import (
    validate_person_name,
    validate_yemeni_phone,
)


# =========================================================
# نموذج العميل
# =========================================================

class CustomerForm(forms.ModelForm):

    full_name = forms.CharField(
        validators=[validate_person_name],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "أدخل الاسم الكامل",
        }),
    )

    phone = forms.CharField(
        validators=[validate_yemeni_phone],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "أدخل رقم الهاتف",
        }),
    )

    class Meta:

        model = Customer

        fields = [
            "full_name",
            "phone",
            "email",
            "address",
            "notes",
        ]

        labels = {

            "full_name": "الاسم الكامل",
            "phone": "رقم الهاتف",
            "email": "البريد الإلكتروني",
            "address": "العنوان",
            "notes": "ملاحظات",

        }

        widgets = {

            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "أدخل الاسم الكامل",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "أدخل رقم الهاتف",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "أدخل البريد الإلكتروني",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "أدخل العنوان",
                    "rows": 3,
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "أدخل الملاحظات",
                    "rows": 3,
                }
            ),

        }


# =========================================================
# نموذج طلب العميل
# =========================================================

class CustomerOrderForm(forms.ModelForm):

    class Meta:

        model = CustomerOrder

        fields = [
            "notes",
        ]

        labels = {
            "notes": "ملاحظات",
        }

        widgets = {

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "أضف ملاحظات للطلب إن وجدت...",
                }
            ),

        }


# =========================================================
# نموذج منتجات طلب العميل
# =========================================================

class CustomerOrderItemForm(forms.ModelForm):

    class Meta:

        model = CustomerOrderItem

        fields = [
            "medicine",
            "quantity",
        ]

        labels = {

            "medicine": "الدواء",
            "quantity": "الكمية",

        }

        widgets = {

            "medicine": forms.Select(
                attrs={
                    "class": "form-select customer-medicine-select",
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # العميل يستطيع اختيار المنتجات المتاحة فقط
        self.fields["medicine"].queryset = Medicine.objects.filter(
            status="available"
        ).order_by("name")


    def clean_quantity(self):

        quantity = self.cleaned_data.get("quantity")

        if quantity is not None and quantity <= 0:

            raise forms.ValidationError(
                "يجب أن تكون الكمية أكبر من صفر."
            )

        return quantity


# =========================================================
# Formset لمنتجات طلب العميل
# =========================================================

CustomerOrderItemFormSet = inlineformset_factory(

    CustomerOrder,

    CustomerOrderItem,

    form=CustomerOrderItemForm,

    extra=1,

    can_delete=True,

)