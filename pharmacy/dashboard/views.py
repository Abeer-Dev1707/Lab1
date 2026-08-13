from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from categories.models import Category
from accounts.models import User


# =========================================================
# تسجيل الدخول
# =========================================================

def login_view(request):

    # إذا كان المستخدم مسجلاً دخوله بالفعل
    if request.user.is_authenticated:

        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        # ==========================================
        # البحث عن الحساب أولًا
        # ==========================================

        try:

            user = User.objects.get(
                username=username
            )

        except User.DoesNotExist:

            messages.error(
                request,
                "اسم المستخدم أو كلمة المرور غير صحيحة."
            )

            return render(
                request,
                "dashboard/login.html"
            )

        # ==========================================
        # التحقق من حالة الحساب
        # ==========================================

        if user.account_status == "pending":

            messages.warning(
                request,
                "⏳ حسابك قيد المراجعة. "
                "يرجى انتظار موافقة المدير قبل تسجيل الدخول."
            )

            return render(
                request,
                "dashboard/login.html"
            )

        if user.account_status == "rejected":

            messages.error(
                request,
                "🚫 تم رفض طلب إنشاء حسابك. "
                "يرجى التواصل مع إدارة الصيدلية."
            )

            return render(
                request,
                "dashboard/login.html"
            )

        # ==========================================
        # التحقق من اسم المستخدم وكلمة المرور
        # ==========================================

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # ======================================
            # التحقق من أن الحساب فعال
            # ======================================

            if not user.is_active:

                messages.error(
                    request,
                    "🚫 هذا الحساب غير نشط حاليًا."
                )

                return render(
                    request,
                    "dashboard/login.html"
                )

            # ======================================
            # التحقق من أن الحساب مقبول
            # ======================================

            if user.account_status != "approved":

                messages.warning(
                    request,
                    "⏳ لا يمكنك الدخول قبل الموافقة على حسابك."
                )

                return render(
                    request,
                    "dashboard/login.html"
                )

            # ======================================
            # تسجيل الدخول
            # ======================================

            login(
                request,
                user
            )

            messages.success(
                request,
                f"مرحباً {user.username}، تم تسجيل الدخول بنجاح."
            )

            return redirect("dashboard")

        else:

            messages.error(
                request,
                "اسم المستخدم أو كلمة المرور غير صحيحة."
            )

    return render(
        request,
        "dashboard/login.html"
    )


# =========================================================
# لوحة التحكم
# =========================================================

@login_required(login_url="login")
def home(request):

    categories = Category.objects.all()

    context = {
        "categories": categories,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )


# =========================================================
# من نحن
# =========================================================

def about(request):

    return render(
        request,
        "dashboard/about.html"
    )


# =========================================================
# اتصل بنا
# =========================================================

def contact(request):

    return render(
        request,
        "dashboard/contact.html"
    )


# =========================================================
# صفحة 404
# =========================================================

def page_not_found(request):

    return render(
        request,
        "404.html"
    )


# =========================================================
# نسيت كلمة المرور
# =========================================================

def forgot_password(request):

    return render(
        request,
        "dashboard/forgot_password.html"
    )


# =========================================================
# تسجيل الخروج
# =========================================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "تم تسجيل الخروج بنجاح."
    )

    return redirect("login")