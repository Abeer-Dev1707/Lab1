from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta

from medicines.models import Medicine
from medicines.forms import MedicineForm

from accounts.decorators import pharmacist_required


# =========================================================
# قائمة المخزون
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def inventory_list(request):

    medicines = Medicine.objects.select_related(
        "category",
        "product_type",
        "supplier"
    ).all()

    today = timezone.now().date()

    warning_date = today + timedelta(days=30)

    # =====================================================
    # تحديد حالة كل دواء
    # =====================================================

    for medicine in medicines:

        # -------------------------
        # حالة المخزون
        # -------------------------

        if medicine.quantity == 0:

            medicine.stock_status = "out"

        elif medicine.quantity <= medicine.minimum_stock:

            medicine.stock_status = "low"

        else:

            medicine.stock_status = "available"

        # -------------------------
        # حالة الصلاحية
        # -------------------------

        if medicine.expiry_date < today:

            medicine.expiry_status = "expired"

        elif medicine.expiry_date <= warning_date:

            medicine.expiry_status = "warning"

        else:

            medicine.expiry_status = "valid"

    return render(
        request,
        "inventory/inventory_list.html",
        {
            "medicines": medicines,
        }
    )


# =========================================================
# تفاصيل الدواء والمخزون
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def inventory_detail(request, pk):

    medicine = get_object_or_404(
        Medicine.objects.select_related(
            "category",
            "product_type",
            "supplier"
        ),
        pk=pk
    )

    today = timezone.now().date()

    warning_date = today + timedelta(days=30)

    # =====================================================
    # حالة المخزون
    # =====================================================

    if medicine.quantity == 0:

        medicine.stock_status = "out"

    elif medicine.quantity <= medicine.minimum_stock:

        medicine.stock_status = "low"

    else:

        medicine.stock_status = "available"


    # =====================================================
    # حالة الصلاحية
    # =====================================================

    if medicine.expiry_date < today:

        medicine.expiry_status = "expired"

    elif medicine.expiry_date <= warning_date:

        medicine.expiry_status = "warning"

    else:

        medicine.expiry_status = "valid"


    return render(
        request,
        "inventory/inventory_detail.html",
        {
            "medicine": medicine,
        }
    )


# =========================================================
# إضافة دواء
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def inventory_create(request):

    if request.method == "POST":

        form = MedicineForm(request.POST)

        if form.is_valid():

            medicine = form.save()

            messages.success(
                request,
                "تمت إضافة الدواء بنجاح."
            )

            return redirect(
                "inventory_detail",
                pk=medicine.pk
            )

    else:

        form = MedicineForm()


    return render(
        request,
        "inventory/inventory_form.html",
        {
            "form": form,
            "page_title": "إضافة دواء"
        }
    )


# =========================================================
# تعديل الدواء
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def inventory_update(request, pk):

    medicine = get_object_or_404(
        Medicine,
        pk=pk
    )


    if request.method == "POST":

        form = MedicineForm(
            request.POST,
            instance=medicine
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "تم تعديل بيانات الدواء بنجاح."
            )

            return redirect(
                "inventory_detail",
                pk=medicine.pk
            )

    else:

        form = MedicineForm(
            instance=medicine
        )


    return render(
        request,
        "inventory/inventory_form.html",
        {
            "form": form,
            "page_title": "تعديل الدواء"
        }
    )