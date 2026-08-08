from django import forms
from .models import ProductType


class ProductTypeForm(forms.ModelForm):

    class Meta:

        model = ProductType

        fields = [
            "name",
            "description",
        ]

        labels = {
            "name": "اسم نوع المنتج",
            "description": "الوصف",
        }

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "أدخل اسم نوع المنتج"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "أدخل وصفاً اختيارياً"
                }
            ),

        }