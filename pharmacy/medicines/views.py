from django.shortcuts import render
from .models import Medicine
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MedicineForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta


def medicine_list(request):

    search = request.GET.get('search', '')

    medicines = Medicine.objects.select_related('category').all()

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

    return render(request, 'medicines/medicine_list.html', {

        'medicines': medicines,
        'search': search,

    })

def medicine_create(request):

    if request.method == 'POST':

        form = MedicineForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "تمت إضافة الدواء بنجاح.")

            return redirect('medicine_list')

    else:

        form = MedicineForm()

    return render(request, 'medicines/medicine_form.html', {
        'form': form,
        'page_title': 'إضافة دواء'
    })

def medicine_update(request, pk):

    medicine = get_object_or_404(Medicine, pk=pk)

    if request.method == "POST":

        form = MedicineForm(request.POST, instance=medicine)

        if form.is_valid():

            form.save()

            messages.success(request, "تم تعديل الدواء بنجاح.")

            return redirect("medicine_list")

    else:

        form = MedicineForm(instance=medicine)

    return render(request, "medicines/medicine_form.html", {

        "form": form,

        "page_title": "تعديل الدواء"

    })

def medicine_delete(request, pk):

    medicine = get_object_or_404(Medicine, pk=pk)

    if request.method == "POST":

        medicine.delete()

        messages.success(request, "تم حذف الدواء بنجاح.")

        return redirect("medicine_list")

    return render(request, "medicines/medicine_delete.html", {
        "medicine": medicine
    })