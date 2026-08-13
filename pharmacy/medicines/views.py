from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

from .models import Medicine
from .forms import MedicineForm

from accounts.decorators import pharmacist_required
from suppliers.models import Supplier


# =========================================================
# قائمة الأدوية
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def medicine_list(request):

    search = request.GET.get('search', '')

    medicines = Medicine.objects.select_related(
        'category',
        'supplier'
    ).all()

    if search:

        medicines = medicines.filter(

            Q(name__icontains=search) |
            Q(barcode__icontains=search) |
            Q(manufacturer__icontains=search) |
            Q(category__name__icontains=search)

        )

    # -------------------------
    # حالة الصلاحية
    # -------------------------

    today = timezone.now().date()

    for medicine in medicines:

        if medicine.expiry_date < today:

            medicine.expiry_status = "expired"

        elif medicine.expiry_date <= today + timedelta(days=30):

            medicine.expiry_status = "warning"

        else:

            medicine.expiry_status = "valid"

    # -------------------------
    # Pagination
    # -------------------------

    paginator = Paginator(medicines, 10)

    page_number = request.GET.get("page")

    medicines = paginator.get_page(page_number)

    return render(
        request,
        'medicines/medicine_list.html',
        {
            'medicines': medicines,
            'search': search,
        }
    )


# =========================================================
# إضافة دواء
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def medicine_create(request):

    if request.method == 'POST':

        form = MedicineForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "تمت إضافة الدواء بنجاح."
            )

            return redirect('medicine_list')

    else:

        form = MedicineForm()

    return render(
        request,
        'medicines/medicine_form.html',
        {
            'form': form,
            'page_title': 'إضافة دواء'
        }
    )


# =========================================================
# تعديل الدواء
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def medicine_update(request, pk):

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
                "تم تعديل الدواء بنجاح."
            )

            return redirect("medicine_list")

    else:

        form = MedicineForm(
            instance=medicine
        )

    return render(
        request,
        "medicines/medicine_form.html",
        {
            "form": form,
            "page_title": "تعديل الدواء"
        }
    )


# =========================================================
# حذف الدواء
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def medicine_delete(request, pk):

    medicine = get_object_or_404(
        Medicine,
        pk=pk
    )

    if request.method == "POST":

        medicine.delete()

        messages.success(
            request,
            "تم حذف الدواء بنجاح."
        )

        return redirect("medicine_list")

    return render(
        request,
        "medicines/medicine_delete.html",
        {
            "medicine": medicine
        }
    )


# =========================================================
# منتجاتي للمورد
# المورد فقط
# =========================================================

@login_required(login_url="login")
def supplier_medicines(request):

    # -----------------------------------------------------
    # التأكد أن المستخدم مورد
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
    # جلب منتجات هذا المورد فقط
    # -----------------------------------------------------

    search = request.GET.get(
        "search",
        ""
    )

    medicines = Medicine.objects.filter(
        supplier=supplier
    ).select_related(
        "category",
        "product_type"
    )


    # -----------------------------------------------------
    # البحث
    # -----------------------------------------------------

    if search:

        medicines = medicines.filter(

            Q(name__icontains=search) |
            Q(barcode__icontains=search) |
            Q(manufacturer__icontains=search) |
            Q(category__name__icontains=search)

        )


    # -----------------------------------------------------
    # حالة الصلاحية
    # -----------------------------------------------------

    today = timezone.now().date()

    for medicine in medicines:

        if medicine.expiry_date < today:

            medicine.expiry_status = "expired"

        elif medicine.expiry_date <= today + timedelta(days=30):

            medicine.expiry_status = "warning"

        else:

            medicine.expiry_status = "valid"


    # -----------------------------------------------------
    # Pagination
    # -----------------------------------------------------

    paginator = Paginator(
        medicines,
        10
    )

    page_number = request.GET.get(
        "page"
    )

    medicines = paginator.get_page(
        page_number
    )


    return render(
        request,
        "medicines/supplier_medicines.html",
        {
            "medicines": medicines,
            "search": search,
        }
    )