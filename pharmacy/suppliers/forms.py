from django import forms
from .models import Supplier
from accounts.validators import (
    validate_person_name,
    validate_yemeni_phone,
    validate_company_name,
)


class SupplierForm(forms.ModelForm):

    full_name = forms.CharField(
        validators=[validate_person_name],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "أدخل اسم المورد",
        }),
    )

    phone = forms.CharField(
        validators=[validate_yemeni_phone],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "أدخل رقم الهاتف",
        }),
    )

    company_name = forms.CharField(
        required=False,
        validators=[validate_company_name],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "أدخل اسم الشركة",
        }),
    )

    class Meta:

        model = Supplier

        fields = [
            "full_name",
            "phone",
            "email",
            "company_name",
            "address",
            "notes",
        ]

        labels = {

            "full_name": "اسم المورد",

            "phone": "رقم الهاتف",

            "email": "البريد الإلكتروني",

            "company_name": "اسم الشركة",

            "address": "العنوان",

            "notes": "ملاحظات",

        }

        widgets = {

            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "أدخل اسم المورد",
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

            "company_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "أدخل اسم الشركة",
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