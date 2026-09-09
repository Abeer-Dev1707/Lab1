from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Max
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

from .models import Medicine
from .forms import MedicineForm, SearchMedicineForm

from accounts.decorators import pharmacist_required
from suppliers.models import Supplier
from purchases.models import PurchaseItem

from notifications.services import notify_admins_and_pharmacists


# =========================================================
# قائمة الأدوية
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def medicine_list(request):

    search = request.GET.get("search", "")

    # =====================================================
    # QuerySet 1
    # all()
    # =====================================================

    medicines = Medicine.objects.select_related(
        "category",
        "supplier",
        "product_type"
    ).all()


    # =====================================================
    # QuerySet 2
    # filter()
    # =====================================================

    if search:

        medicines = medicines.filter(

            Q(name__icontains=search) |
            Q(barcode__icontains=search) |
            Q(manufacturer__icontains=search) |
            Q(category__name__icontains=search)

        )


    # =====================================================
    # QuerySet 3
    # count()
    # =====================================================

    medicine_count = medicines.count()


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

    page_number = request.GET.get("page")

    medicines = paginator.get_page(
        page_number
    )


    return render(
        request,
        "medicines/medicine_list.html",
        {
            "medicines": medicines,
            "search": search,
            "medicine_count": medicine_count,
        }
    )


# =========================================================
# إضافة دواء
# ModelForm
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def medicine_create(request):

    if request.method == "POST":

        form = MedicineForm(request.POST)

        if form.is_valid():

            medicine = form.save()

            # =============================================
            # إشعار المدير والصيدلي بإضافة دواء جديد
            # =============================================

            notify_admins_and_pharmacists(
                title="تمت إضافة دواء جديد",
                message=(
                    f"تمت إضافة الدواء "
                    f"{medicine.name} "
                    f"إلى قائمة الأدوية."
                ),
                notification_type="medicine"
            )

            messages.success(
                request,
                "تمت إضافة الدواء بنجاح."
            )

            return redirect("medicine_list")

    else:

        form = MedicineForm()

    return render(
        request,
        "medicines/medicine_form.html",
        {
            "form": form,
            "page_title": "إضافة دواء"
        }
    )


# =========================================================
# تعديل الدواء
# ModelForm
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

            medicine = form.save()

            # =============================================
            # إشعار المدير والصيدلي بتعديل دواء
            # =============================================

            notify_admins_and_pharmacists(
                title="تم تعديل دواء",
                message=(
                    f"تم تعديل بيانات الدواء "
                    f"{medicine.name}."
                ),
                notification_type="medicine"
            )

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
            "page_title": "تعديل دواء"
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

        medicine_name = medicine.name

        medicine.delete()

        # =============================================
        # إشعار المدير والصيدلي بحذف دواء
        # =============================================

        notify_admins_and_pharmacists(
            title="تم حذف دواء",
            message=(
                f"تم حذف الدواء "
                f"{medicine_name} "
                f"من قائمة الأدوية."
            ),
            notification_type="medicine"
        )

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
    # الحصول على المورد المرتبط بالحساب
    # -----------------------------------------------------

    supplier = get_object_or_404(
        Supplier,
        user=request.user
    )


    # -----------------------------------------------------
    # البحث
    # -----------------------------------------------------

    search = request.GET.get(
        "search",
        ""
    ).strip()


    # =====================================================
    # المنتجات التي قام هذا المورد بتوريدها فعليًا
    # =====================================================

    medicines = Medicine.objects.filter(

        purchase_items__order__supplier=supplier,

        purchase_items__order__status="completed"

    ).select_related(

        "category",
        "product_type",
        "supplier"

    ).annotate(

        supplied_quantity=Sum(
            "purchase_items__quantity",
            filter=Q(
                purchase_items__order__supplier=supplier,
                purchase_items__order__status="completed"
            )
        ),

        last_supply_date=Max(
            "purchase_items__order__created_at",
            filter=Q(
                purchase_items__order__supplier=supplier,
                purchase_items__order__status="completed"
            )
        )

    ).distinct()


    # =====================================================
    # QuerySet 4
    # filter()
    # =====================================================

    if search:

        medicines = medicines.filter(

            Q(name__icontains=search) |

            Q(barcode__icontains=search) |

            Q(manufacturer__icontains=search) |

            Q(category__name__icontains=search)

        )


    # =====================================================
    # QuerySet 5
    # order_by()
    # =====================================================

    medicines = medicines.order_by(
        "-last_supply_date",
        "name"
    )


    # =====================================================
    # QuerySet 6
    # distinct()
    # =====================================================


    # =====================================================
    # QuerySet 7
    # count()
    # =====================================================

    supplier_medicine_count = medicines.count()


    # =====================================================
    # QuerySet 8
    # aggregate()
    # =====================================================

    supplier_totals = medicines.aggregate(
        total_quantity=Sum("supplied_quantity")
    )

    supplier_total_quantity = (
        supplier_totals["total_quantity"] or 0
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


    # -----------------------------------------------------
    # عرض الصفحة
    # -----------------------------------------------------

    return render(
        request,
        "medicines/supplier_medicines.html",
        {
            "medicines": medicines,
            "search": search,
            "supplier": supplier,

            "supplier_medicine_count": supplier_medicine_count,
            "supplier_total_quantity": supplier_total_quantity,
        }
    )


# =========================================================
# الطريقة الثانية للفورم
# forms.Form
# =========================================================

@pharmacist_required
def django_form(request):

    form = SearchMedicineForm(
        request.GET or None
    )

    results = Medicine.objects.all()

    if form.is_valid():

        search = form.cleaned_data.get(
            "search"
        )

        if search:

            results = results.filter(

                Q(name__icontains=search) |

                Q(barcode__icontains=search)

            )

    return render(
        request,
        "medicines/django_form.html",
        {
            "form": form,
            "results": results,
        }
    )


# =========================================================
# الطريقة الأولى للفورم
# HTML Form عادي
# =========================================================

@pharmacist_required
def simple_html_form(request):

    results = Medicine.objects.all()

    search = ""

    if request.method == "POST":

        search = request.POST.get(
            "search",
            ""
        ).strip()

        if search:

            results = results.filter(

                Q(name__icontains=search) |

                Q(barcode__icontains=search)

            )

    return render(
        request,
        "medicines/simple_html_form.html",
        {
            "results": results,
            "search": search,
        }
    )