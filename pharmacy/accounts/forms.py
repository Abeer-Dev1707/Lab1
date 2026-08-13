from django import forms
from .models import User


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

            "password": forms.PasswordInput(
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