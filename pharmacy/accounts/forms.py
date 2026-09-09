from django import forms
from .models import User
from .validators import (
    validate_person_name,
    validate_project_username,
    validate_yemeni_phone,
)

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password


# =========================================================
# نموذج تسجيل حساب جديد
# يستخدمه الصيدلي / العميل / المورد عند التسجيل بأنفسهم
# =========================================================

class RegistrationForm(forms.ModelForm):

    password = forms.CharField(
        label="كلمة المرور",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "أدخل كلمة المرور",
                "autocomplete": "new-password",
                "value": ""
            }
        )
    )

    full_name = forms.CharField(
        validators=[validate_person_name],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "أدخل الاسم الكامل",
        }),
    )

    username = forms.CharField(
        validators=[validate_project_username],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "أدخل اسم المستخدم",
            "autocomplete": "new-username",
        }),
    )

    phone = forms.CharField(
        validators=[validate_yemeni_phone],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "أدخل رقم الهاتف",
            "autocomplete": "off",
        }),
    )

    password_confirm = forms.CharField(
        label="تأكيد كلمة المرور",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "أعد إدخال كلمة المرور",
                "autocomplete": "new-password",
                "value": ""
            }
        )
    )

    class Meta:

        model = User

        fields = [
            "full_name",
            "username",
            "email",
            "phone",
            "role",
        ]

        labels = {
            "full_name": "الاسم الكامل",
            "username": "اسم المستخدم",
            "email": "البريد الإلكتروني",
            "phone": "رقم الهاتف",
            "role": "نوع الحساب",
        }

        widgets = {

            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "أدخل الاسم الكامل"
                }
            ),

            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "أدخل اسم المستخدم",
                    "autocomplete": "new-username",
                    "value": ""
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "أدخل البريد الإلكتروني",
                    "autocomplete": "off"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "أدخل رقم الهاتف",
                    "autocomplete": "off"
                }
            ),

            "role": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),
        }

    # =====================================================
    # منع إنشاء حساب مدير من صفحة التسجيل العامة
    # =====================================================

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["role"].choices = [
            ("pharmacist", "صيدلي"),
            ("customer", "عميل"),
            ("supplier", "مورد"),
        ]

    def clean_password(self):

        password = self.cleaned_data.get("password")

        if password:
            validate_password(password, self.instance)

        return password

    # =====================================================
    # التحقق من تطابق كلمتي المرور
    # =====================================================

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm:

            if password != password_confirm:

                raise forms.ValidationError(
                    "كلمتا المرور غير متطابقتين."
                )

        return cleaned_data


# =========================================================
# نموذج إدارة المستخدمين من المدير
# =========================================================

class UserForm(forms.ModelForm):

    password = forms.CharField(
        label="كلمة المرور",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "اترك الحقل فارغًا إذا لم ترد تغيير كلمة المرور",
                "autocomplete": "new-password"
            }
        )
    )

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

            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "أدخل اسم المستخدم",
                    "autocomplete": "new-username",
                    "value": ""
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "role": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }

        # =========================================================
# نموذج تغيير كلمة المرور
# =========================================================

class UserPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label="كلمة المرور الحالية",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "أدخل كلمة المرور الحالية",
                "autocomplete": "current-password"
            }
        )
    )

    new_password1 = forms.CharField(
        label="كلمة المرور الجديدة",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "أدخل كلمة المرور الجديدة",
                "autocomplete": "new-password"
            }
        )
    )

    new_password2 = forms.CharField(
        label="تأكيد كلمة المرور الجديدة",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "أعد إدخال كلمة المرور الجديدة",
                "autocomplete": "new-password"
            }
        )
    )