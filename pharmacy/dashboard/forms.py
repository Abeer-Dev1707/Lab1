from django import forms


class ContactForm(forms.Form):

    # ==========================================
    # بيانات المرسل
    # ==========================================

    name = forms.CharField(
        label="اسم المرسل",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "أدخل اسم المرسل",
                "autocomplete": "name",
            }
        ),
    )

    email = forms.EmailField(
        label="بريد المرسل",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "أدخل بريد المرسل",
                "autocomplete": "email",
            }
        ),
    )

    # ==========================================
    # بيانات المستقبل
    # ==========================================

    recipient_name = forms.CharField(
        label="اسم المستقبل",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "أدخل اسم المستقبل",
                "autocomplete": "name",
            }
        ),
    )

    recipient_email = forms.EmailField(
        label="بريد المستقبل",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "أدخل بريد المستقبل",
                "autocomplete": "email",
            }
        ),
    )

    # ==========================================
    # الرسالة
    # ==========================================

    message = forms.CharField(
        label="الرسالة",
        max_length=5000,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "اكتب الرسالة هنا...",
                "rows": 6,
            }
        ),
    )