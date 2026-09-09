from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Supplier
from .forms import SupplierForm

from accounts.decorators import pharmacist_required

from notifications.models import Notification
from notifications.services import notify_admins_and_pharmacists


# =========================================================
# قائمة الموردين
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def supplier_list(request):

    search = request.GET.get("search", "")

    suppliers = Supplier.objects.all()

    if search:

        suppliers = suppliers.filter(

            Q(full_name__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search) |
            Q(company_name__icontains=search) |
            Q(address__icontains=search)

        )

    paginator = Paginator(suppliers, 10)

    page_number = request.GET.get("page")

    suppliers = paginator.get_page(page_number)

    return render(
        request,
        "suppliers/supplier_list.html",
        {
            "suppliers": suppliers,
            "search": search,
        }
    )


# =========================================================
# إضافة مورد
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def supplier_create(request):

    if request.method == "POST":

        form = SupplierForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "تمت إضافة المورد بنجاح."
            )

            return redirect("supplier_list")

    else:

        form = SupplierForm()

    return render(
        request,
        "suppliers/supplier_form.html",
        {
            "form": form,
            "page_title": "إضافة مورد",
        }
    )


# =========================================================
# تعديل المورد
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def supplier_update(request, pk):

    supplier = get_object_or_404(
        Supplier,
        pk=pk
    )

    if request.method == "POST":

        form = SupplierForm(
            request.POST,
            instance=supplier
        )

        if form.is_valid():

            form.save()

            # =========================================
            # إشعار المورد بتعديل بيانات حسابه
            # =========================================

            if supplier.user:

                Notification.objects.create(
                    user=supplier.user,
                    title="تم تعديل بيانات حسابك",
                    message=(
                        "تم تعديل بيانات حسابك "
                        "من قبل إدارة الصيدلية."
                    ),
                    notification_type="profile"
                )

            # =========================================
            # إشعار المدير والصيدلي بتعديل بيانات المورد
            # =========================================

            notify_admins_and_pharmacists(
                title="تم تعديل بيانات مورد",
                message=(
                    f"تم تعديل بيانات المورد "
                    f"{supplier.full_name} "
                    f"من قبل إدارة الصيدلية."
                ),
                notification_type="profile"
            )

            messages.success(
                request,
                "تم تعديل بيانات المورد بنجاح."
            )

            return redirect("supplier_list")

    else:

        form = SupplierForm(
            instance=supplier
        )

    return render(
        request,
        "suppliers/supplier_form.html",
        {
            "form": form,
            "page_title": "تعديل المورد",
        }
    )


# =========================================================
# حذف المورد
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def supplier_delete(request, pk):

    supplier = get_object_or_404(
        Supplier,
        pk=pk
    )

    if request.method == "POST":

        supplier.delete()

        messages.success(
            request,
            "تم حذف المورد بنجاح."
        )

        return redirect("supplier_list")

    return render(
        request,
        "suppliers/supplier_delete.html",
        {
            "supplier": supplier,
        }
    )


# =========================================================
# بياناتي للمورد
# المورد فقط
# =========================================================

@login_required(login_url="login")
def supplier_profile(request):

    # -----------------------------------------------------
    # التأكد أن المستخدم الحالي مورد
    # -----------------------------------------------------

    if request.user.role != "supplier":

        messages.error(
            request,
            "🚫 غير مسموح لك بالوصول إلى هذه الصفحة."
        )

        return redirect("dashboard")


    # -----------------------------------------------------
    # الحصول على ملف المورد المرتبط بالحساب
    # -----------------------------------------------------

    supplier = get_object_or_404(
        Supplier,
        user=request.user
    )


    # -----------------------------------------------------
    # تعديل بيانات المورد
    # -----------------------------------------------------

    if request.method == "POST":

        form = SupplierForm(
            request.POST,
            instance=supplier
        )

        if form.is_valid():

            form.save()

            # =============================================
            # إشعار بتحديث البيانات الشخصية
            # =============================================

            Notification.objects.create(
                user=request.user,
                title="تم تحديث بياناتك",
                message=(
                    "تم تحديث بيانات ملفك الشخصي بنجاح."
                ),
                notification_type="profile"
            )

            # =============================================
            # إشعار المدير والصيدلي بتحديث بيانات المورد
            # =============================================

            notify_admins_and_pharmacists(
                title="تم تحديث بيانات مورد",
                message=(
                    f"قام المورد {supplier.full_name} "
                    f"بتحديث بيانات ملفه الشخصي."
                ),
                notification_type="profile"
            )

            messages.success(
                request,
                "تم تحديث بياناتك بنجاح."
            )

            return redirect("supplier_profile")

    else:

        form = SupplierForm(
            instance=supplier
        )


    return render(
        request,
        "suppliers/supplier_profile.html",
        {
            "form": form,
            "supplier": supplier,
        }
    )
