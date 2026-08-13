from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import User
from customers.models import Customer
from .forms import UserForm, RegistrationForm
from .decorators import admin_required
from suppliers.models import Supplier


# =========================================================
# إدارة المستخدمين - المدير
# =========================================================

@admin_required
def user_list(request):

    search = request.GET.get("search", "")

    users = User.objects.all()

    if search:

        users = users.filter(

            Q(full_name__icontains=search) |
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)

        )

    paginator = Paginator(users, 10)

    page_number = request.GET.get("page")

    users = paginator.get_page(page_number)

    return render(
        request,
        "accounts/user_list.html",
        {
            "users": users,
            "search": search,
        }
    )


# =========================================================
# إنشاء حساب من المدير
# =========================================================

@admin_required
def user_create(request):

    if request.method == "POST":

        form = UserForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # تشفير كلمة المرور
            user.set_password(
                form.cleaned_data["password"]
            )

            # الحساب الذي ينشئه المدير يكون مقبولًا مباشرة
            user.account_status = "approved"
            user.is_active = True

            user.save()

            messages.success(
                request,
                "تم إنشاء حساب المستخدم بنجاح."
            )

            return redirect("user_list")

    else:

        form = UserForm()

    return render(
        request,
        "accounts/user_form.html",
        {
            "form": form,
            "page_title": "إنشاء حساب",
        }
    )


# =========================================================
# تعديل المستخدم من المدير
# =========================================================

@admin_required
def user_update(request, pk):

    user = get_object_or_404(
        User,
        pk=pk
    )

    if request.method == "POST":

        form = UserForm(
            request.POST,
            instance=user
        )

        if form.is_valid():

            updated_user = form.save(
                commit=False
            )

            # تشفير كلمة المرور الجديدة
            updated_user.set_password(
                form.cleaned_data["password"]
            )

            updated_user.save()

            messages.success(
                request,
                "تم تعديل المستخدم بنجاح."
            )

            return redirect("user_list")

    else:

        form = UserForm(
            instance=user
        )

    return render(
        request,
        "accounts/user_form.html",
        {
            "form": form,
            "page_title": "تعديل المستخدم",
        }
    )


# =========================================================
# حذف المستخدم
# =========================================================

@admin_required
def user_delete(request, pk):

    user = get_object_or_404(
        User,
        pk=pk
    )

    if request.method == "POST":

        user.delete()

        messages.success(
            request,
            "تم حذف المستخدم بنجاح."
        )

        return redirect("user_list")

    return render(
        request,
        "accounts/user_delete.html",
        {
            "user": user
        }
    )


# =========================================================
# التسجيل العام
# صيدلي / عميل / مورد
# =========================================================

def register(request):

    # إذا كان المستخدم مسجلًا بالفعل
    if request.user.is_authenticated:

        return redirect("dashboard")

    if request.method == "POST":

        form = RegistrationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save(
                commit=False
            )

            # -----------------------------------------
            # تشفير كلمة المرور
            # -----------------------------------------

            user.set_password(
                form.cleaned_data["password"]
            )

            # -----------------------------------------
            # الحساب ينتظر موافقة المدير
            # -----------------------------------------

            user.account_status = "pending"

            # لا يستطيع الدخول قبل الموافقة
            user.is_active = False

            user.save()

            messages.success(
                request,
                "تم إرسال طلب إنشاء الحساب بنجاح. "
                "سيتمكن من الدخول بعد موافقة المدير."
            )

            return redirect("login")

    else:

        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
            "page_title": "إنشاء حساب",
        }
    )



# =========================================================
# طلبات الحسابات - المدير
# =========================================================

@admin_required
def account_requests(request):

    requests = User.objects.filter(
        account_status="pending"
    ).order_by("-created_at")

    return render(
        request,
        "accounts/account_requests.html",
        {
            "requests": requests
        }
    )


# =========================================================
# الموافقة على الحساب
# =========================================================

@admin_required
def approve_account(request, pk):

    user = get_object_or_404(
        User,
        pk=pk
    )

    if request.method == "POST":

        # -----------------------------------------
        # الموافقة على الحساب
        # -----------------------------------------

        user.account_status = "approved"
        user.is_active = True

        user.save()

        # -----------------------------------------
        # إنشاء ملف العميل تلقائيًا
        # -----------------------------------------

        if user.role == "customer":

            Customer.objects.get_or_create(

                user=user,

                defaults={
                    "full_name": user.full_name,
                    "phone": user.phone,
                    "email": user.email,
                }

            )

        # -----------------------------------------
        # إنشاء ملف المورد تلقائيًا
        # -----------------------------------------

        elif user.role == "supplier":

            Supplier.objects.get_or_create(

                user=user,

                defaults={
                    "full_name": user.full_name,
                    "phone": user.phone,
                    "email": user.email,
                }

            )

        messages.success(
            request,
            f"تمت الموافقة على حساب {user.full_name}."
        )

    return redirect("account_requests")


# =========================================================
# طلبات الحسابات - المدير
# =========================================================

@admin_required
def account_requests(request):

    requests = User.objects.filter(
        account_status="pending"
    ).order_by("-created_at")

    return render(
        request,
        "accounts/account_requests.html",
        {
            "requests": requests
        }
    )


# =========================================================
# طلبات الحسابات - المدير
# =========================================================

@admin_required
def approve_account(request, pk):

    user = get_object_or_404(
        User,
        pk=pk
    )

    if request.method == "POST":

        # -----------------------------------------
        # الموافقة على الحساب
        # -----------------------------------------

        user.account_status = "approved"
        user.is_active = True

        user.save()

        # -----------------------------------------
        # إنشاء ملف العميل تلقائيًا
        # -----------------------------------------

        if user.role == "customer":

            Customer.objects.get_or_create(

                user=user,

                defaults={
                    "full_name": user.full_name,
                    "phone": user.phone,
                    "email": user.email,
                }

            )

        # -----------------------------------------
        # إنشاء ملف المورد تلقائيًا
        # -----------------------------------------

        elif user.role == "supplier":

            Supplier.objects.get_or_create(

                user=user,

                defaults={
                    "full_name": user.full_name,
                    "phone": user.phone,
                    "email": user.email,
                }

            )

        messages.success(
            request,
            f"تمت الموافقة على حساب {user.full_name}."
        )

    return redirect("account_requests")

# =========================================================
# رفض الحساب
# =========================================================

@admin_required
def reject_account(request, pk):

    user = get_object_or_404(
        User,
        pk=pk
    )

    if request.method == "POST":

        user.account_status = "rejected"
        user.is_active = False

        user.save()

        messages.warning(
            request,
            f"تم رفض طلب حساب {user.full_name}."
        )

    return redirect("account_requests")