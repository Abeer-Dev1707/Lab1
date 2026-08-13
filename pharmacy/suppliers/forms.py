from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):

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