from django import forms
from .models import User


class UserForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            "full_name",
            "username",
            "email",
            "phone",
            "password",
            "role",
            "is_active",
        ]

        labels = {

            "full_name": "الاسم الكامل",

            "username": "اسم المستخدم",

            "email": "البريد الإلكتروني",

            "phone": "رقم الهاتف",

            "password": "كلمة المرور",

            "role": "الدور",

            "is_active": "الحالة",

        }

        widgets = {

            "full_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "username": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "password": forms.PasswordInput(attrs={
                "class": "form-control"
            }),

            "role": forms.Select(attrs={
                "class": "form-select"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

        }