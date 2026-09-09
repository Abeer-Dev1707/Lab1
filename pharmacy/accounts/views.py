from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import User
from customers.models import Customer
from .forms import UserForm, RegistrationForm
from .decorators import admin_required
from suppliers.models import Supplier

from notifications.services import (
    notify_admins,
    notify_user,
)

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .forms import (
    UserForm,
    RegistrationForm,
    UserPasswordChangeForm,
)


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

    paginator = Paginator(
        users,
        10
    )

    page_number = request.GET.get("page")

    users = paginator.get_page(
        page_number
    )

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

            user = form.save(
                commit=False
            )

            # تشفير كلمة المرور
            user.set_password(
                form.cleaned_data["password"]
            )

            # الحساب الذي ينشئه المدير يكون مقبولًا مباشرة
            user.account_status = "approved"
            user.is_active = True

            user.save()

            # =========================================
            # إشعار المستخدم بإنشاء الحساب
            # =========================================

            notify_user(
                user=user,
                title="تم إنشاء حسابك",
                message=(
                    "تم إنشاء حسابك من قبل إدارة الصيدلية "
                    "ويمكنك استخدام النظام."
                ),
                notification_type="account"
            )

            messages.success(
                request,
                "تم إنشاء حساب المستخدم بنجاح."
            )

            return redirect(
                "user_list"
            )

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

            # -----------------------------------------
            # التحقق هل تم إدخال كلمة مرور جديدة
            # -----------------------------------------

            new_password = form.cleaned_data.get(
                "password"
            )

            password_changed = bool(
                new_password
            )

            # -----------------------------------------
            # حفظ البيانات بدون تغيير كلمة المرور
            # -----------------------------------------

            updated_user = form.save(
                commit=False
            )

            # -----------------------------------------
            # تغيير كلمة المرور فقط إذا أدخل المدير
            # كلمة مرور جديدة
            # -----------------------------------------

            if password_changed:

                updated_user.set_password(
                    new_password
                )

            # -----------------------------------------
            # حفظ المستخدم
            # -----------------------------------------

            updated_user.save()

            # =========================================
            # إشعار تعديل البيانات
            # =========================================

            notify_user(
                user=updated_user,
                title="تم تعديل بيانات حسابك",
                message=(
                    "تم تعديل بيانات حسابك "
                    "من قبل إدارة الصيدلية."
                ),
                notification_type="profile"
            )

            # =========================================
            # إشعار تغيير كلمة المرور
            # يظهر فقط إذا تم إدخال كلمة مرور جديدة
            # =========================================

            if password_changed:

                notify_user(
                    user=updated_user,
                    title="تم تحديث كلمة المرور",
                    message=(
                        "تم تحديث كلمة المرور الخاصة بحسابك "
                        "من قبل إدارة الصيدلية."
                    ),
                    notification_type="password"
                )

            messages.success(
                request,
                "تم تعديل المستخدم بنجاح."
            )

            return redirect(
                "user_list"
            )

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

        return redirect(
            "user_list"
        )

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

        return redirect(
            "dashboard"
        )

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

            # =========================================
            # إشعار المدير بوجود حساب جديد
            # =========================================

            notify_admins(
                title="حساب جديد",
                message=(
                    f"تم تسجيل حساب جديد باسم "
                    f"{user.full_name} "
                    f"ونوع الحساب: "
                    f"{user.get_role_display()}"
                ),
                notification_type="account"
            )

            messages.success(
                request,
                "تم إرسال طلب إنشاء الحساب بنجاح. "
                "سيتمكن من الدخول بعد موافقة المدير."
            )

            return redirect(
                "login"
            )

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
    ).order_by(
        "-created_at"
    )

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

        # =========================================
        # إشعار المستخدم بالموافقة
        # =========================================

        notify_user(
            user=user,
            title="تمت الموافقة على حسابك",
            message=(
                "تمت الموافقة على حسابك، "
                "ويمكنك الآن تسجيل الدخول إلى النظام."
            ),
            notification_type="approval"
        )

        messages.success(
            request,
            f"تمت الموافقة على حساب {user.full_name}."
        )

    return redirect(
        "account_requests"
    )


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

        # =========================================
        # إشعار المستخدم بالرفض
        # =========================================

        notify_user(
            user=user,
            title="تم رفض حسابك",
            message=(
                "تم رفض طلب إنشاء حسابك. "
                "يرجى التواصل مع إدارة الصيدلية "
                "لمزيد من المعلومات."
            ),
            notification_type="rejection"
        )

        messages.warning(
            request,
            f"تم رفض طلب حساب {user.full_name}."
        )

    return redirect(
        "account_requests"
    )

# =========================================================
# إعدادات الحساب
# جميع المستخدمين المسجلين
# =========================================================

@login_required(login_url="login")
def settings_view(request):

    user = request.user

    password_form = UserPasswordChangeForm(
        user=user
    )

    if request.method == "POST":

        action = request.POST.get(
            "action"
        )

        # =================================================
        # تغيير كلمة المرور
        # =================================================

        if action == "change_password":

            password_form = UserPasswordChangeForm(
                user=user,
                data=request.POST
            )

            if password_form.is_valid():

                password_form.save()

                update_session_auth_hash(
                    request,
                    user
                )

                notify_user(
                    user=user,
                    title="تم تغيير كلمة المرور",
                    message=(
                        "تم تغيير كلمة المرور الخاصة بحسابك "
                        "بنجاح."
                    ),
                    notification_type="password"
                )

                messages.success(
                    request,
                    "تم تغيير كلمة المرور بنجاح."
                )

                return redirect(
                    "settings"
                )

        # =================================================
        # تعديل البيانات الشخصية
        # =================================================

        elif action == "update_profile":

            first_name = request.POST.get(
                "first_name",
                ""
            ).strip()

            last_name = request.POST.get(
                "last_name",
                ""
            ).strip()

            email = request.POST.get(
                "email",
                ""
            ).strip()

            user.first_name = first_name
            user.last_name = last_name
            user.email = email

            # ---------------------------------------------
            # تحديث الاسم الكامل
            # ---------------------------------------------

            full_name = (
                f"{first_name} {last_name}"
            ).strip()

            if full_name:

                user.full_name = full_name

            user.save()

            notify_user(
                user=user,
                title="تم تعديل بيانات حسابك",
                message=(
                    "تم تعديل بيانات حسابك الشخصية "
                    "بنجاح."
                ),
                notification_type="profile"
            )

            messages.success(
                request,
                "تم تعديل بياناتك بنجاح."
            )

            return redirect(
                "settings"

            )

    return render(
        request,
            "dashboard/settings.html",
        {
            "password_form": password_form,
        }
    )


# =========================================================
# تغيير كلمة المرور - رابط مستقل
# =========================================================

@login_required(login_url="login")
def change_password(request):

    if request.method != "POST":

        return redirect(
            "settings"
        )

    password_form = UserPasswordChangeForm(
        user=request.user,
        data=request.POST
    )

    if password_form.is_valid():

        password_form.save()

        update_session_auth_hash(
            request,
            request.user
        )

        notify_user(
            user=request.user,
            title="تم تغيير كلمة المرور",
            message=(
                "تم تغيير كلمة المرور الخاصة بحسابك "
                "بنجاح."
            ),
            notification_type="password"
        )

        messages.success(
            request,
            "تم تغيير كلمة المرور بنجاح."
        )

    else:

        messages.error(
            request,
            "تعذر تغيير كلمة المرور. "
            "يرجى التأكد من البيانات المدخلة."
        )

    return redirect(
        "settings"
    )