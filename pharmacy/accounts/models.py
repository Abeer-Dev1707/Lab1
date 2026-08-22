from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    # ==========================================
    # أنواع المستخدمين
    # ==========================================

    ROLE_CHOICES = [
        ("admin", "مدير"),
        ("pharmacist", "صيدلي"),
        ("customer", "عميل"),
        ("supplier", "مورد"),
    ]

    # ==========================================
    # حالة طلب الحساب
    # ==========================================

    ACCOUNT_STATUS_CHOICES = [
        ("pending", "قيد المراجعة"),
        ("approved", "مقبول"),
        ("rejected", "مرفوض"),
    ]

    # ==========================================
    # البيانات الشخصية
    # ==========================================

    full_name = models.CharField(
        max_length=200,
        verbose_name="الاسم الكامل"
    )

    email = models.EmailField(
        unique=True,
        verbose_name="البريد الإلكتروني"
    )

    phone = models.CharField(
        max_length=20,
        verbose_name="رقم الهاتف"
    )

    # ==========================================
    # نوع الحساب
    # ==========================================

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="pharmacist",
        verbose_name="نوع الحساب"
    )

    # ==========================================
    # حالة الحساب
    # ==========================================

    account_status = models.CharField(
        max_length=20,
        choices=ACCOUNT_STATUS_CHOICES,
        default="pending",
        verbose_name="حالة الحساب"
    )

    # ==========================================
    # حالة النشاط
    # ==========================================

    is_active = models.BooleanField(
        default=True,
        verbose_name="الحساب نشط"
    )

    # ==========================================
    # التواريخ
    # ==========================================

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث"
    )

    # ==========================================
    # عرض اسم المستخدم
    # ==========================================

    def __str__(self):
        return self.full_name or self.username

    # ==========================================
    # معلومات النموذج
    # ==========================================

    class Meta:
        verbose_name = "مستخدم"
        verbose_name_plural = "المستخدمون"
        ordering = ["full_name"]


# =========================================================
# ملف المدير
# =========================================================
# علاقة One-to-One:
#
# User 1 -------- 1 ManagerProfile
#
# كل مستخدم مدير يمكن أن يمتلك ملف مدير واحد فقط.
# =========================================================

class ManagerProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="manager_profile",
        verbose_name="المستخدم"
    )

    job_title = models.CharField(
        max_length=100,
        default="مدير الصيدلية",
        verbose_name="المسمى الوظيفي"
    )

    employee_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="الرقم الوظيفي"
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="العنوان"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ إنشاء الملف"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث"
    )

    def __str__(self):
        return f"ملف المدير: {self.user.full_name}"

    class Meta:
        verbose_name = "ملف مدير"
        verbose_name_plural = "ملفات المديرين"
        ordering = ["id"]