import re

from django.core.exceptions import ValidationError


# =========================================================
# Validators خاصة بنظام الصيدلية
# =========================================================

ARABIC_ENGLISH_NAME_RE = re.compile(
    r"^[\u0600-\u06FFa-zA-Z]+(?:[\u0600-\u06FFa-zA-Z'’.-]*[\u0600-\u06FFa-zA-Z]+)*(?:\s+[\u0600-\u06FFa-zA-Z]+(?:[\u0600-\u06FFa-zA-Z'’.-]*[\u0600-\u06FFa-zA-Z]+)*)*$"
)

PHONE_RE = re.compile(
    r"^(?:\+967|00967|0)?7\d{8}$"
)

USERNAME_RE = re.compile(
    r"^[A-Za-z0-9_.@+-]{3,30}$"
)


# =========================================================
# الاسم
# =========================================================

def validate_person_name(value):

    value = " ".join((value or "").strip().split())

    if len(value) < 2:
        raise ValidationError(
            "يجب أن يحتوي الاسم على حرفين على الأقل."
        )

    if len(value) > 100:
        raise ValidationError(
            "الاسم طويل جدًا. الحد الأقصى 100 حرف."
        )

    if not ARABIC_ENGLISH_NAME_RE.fullmatch(value):
        raise ValidationError(
            "الاسم يجب أن يحتوي على حروف عربية أو إنجليزية ومسافات فقط."
        )

    return value


# =========================================================
# رقم الهاتف اليمني
# =========================================================

def validate_yemeni_phone(value):

    value = (value or "").strip().replace(" ", "")

    if not PHONE_RE.fullmatch(value):
        raise ValidationError(
            "أدخل رقم هاتف يمني صحيح، مثل 771234567 أو +967771234567."
        )

    return value


# =========================================================
# اسم المستخدم
# =========================================================

def validate_project_username(value):

    value = (value or "").strip()

    if not USERNAME_RE.fullmatch(value):
        raise ValidationError(
            "اسم المستخدم يجب أن يكون من 3 إلى 30 خانة، ويحتوي على أحرف إنجليزية أو أرقام أو . _ @ + -."
        )

    return value


# =========================================================
# اسم الشركة / النصوص القصيرة
# =========================================================

def validate_company_name(value):

    value = " ".join((value or "").strip().split())

    if value and len(value) < 2:
        raise ValidationError(
            "اسم الشركة يجب أن يحتوي على حرفين على الأقل."
        )

    if len(value) > 200:
        raise ValidationError(
            "اسم الشركة طويل جدًا."
        )

    return value
