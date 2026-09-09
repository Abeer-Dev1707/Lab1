from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q

from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemFormSet

from accounts.decorators import pharmacist_required

from notifications.services import (
    notify_admins_and_pharmacists,
)


# =========================================================
# قائمة المبيعات
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def sale_list(request):

    search = request.GET.get("search", "")

    sales = Sale.objects.select_related(
        "customer",
        "cashier"
    ).prefetch_related(
        "items__medicine"
    ).all()

    # -----------------------------------------------------
    # البحث
    # -----------------------------------------------------

    if search:

        sales = sales.filter(
            Q(customer__full_name__icontains=search) |
            Q(id__icontains=search)
        )

    return render(
        request,
        "sales/sale_list.html",
        {
            "sales": sales,
            "search": search,
        }
    )


# =========================================================
# إنشاء فاتورة بيع
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def sale_create(request):

    if request.method == "POST":

        sale_form = SaleForm(
            request.POST
        )

        item_formset = SaleItemFormSet(
            request.POST
        )

        # -------------------------------------------------
        # التحقق من الفاتورة والمنتجات
        # -------------------------------------------------

        if (
            sale_form.is_valid()
            and item_formset.is_valid()
        ):

            # -------------------------------------------------
            # التحقق من وجود منتج واحد على الأقل
            # -------------------------------------------------

            valid_items = []

            for form in item_formset:

                if not form.cleaned_data:
                    continue

                if form.cleaned_data.get("DELETE"):
                    continue

                medicine = form.cleaned_data.get(
                    "medicine"
                )

                quantity = form.cleaned_data.get(
                    "quantity"
                )

                if medicine and quantity:

                    valid_items.append(
                        form
                    )


            if not valid_items:

                messages.error(
                    request,
                    "يجب إضافة دواء واحد على الأقل إلى الفاتورة."
                )

                return render(
                    request,
                    "sales/sale_form.html",
                    {
                        "sale_form": sale_form,
                        "item_formset": item_formset,
                    }
                )


            # -------------------------------------------------
            # تنفيذ البيع بالكامل داخل Transaction
            # -------------------------------------------------

            try:

                with transaction.atomic():

                    # =========================================
                    # إنشاء الفاتورة
                    # =========================================

                    sale = sale_form.save(
                        commit=False
                    )

                    sale.cashier = request.user

                    sale.status = "completed"

                    sale.total_amount = 0

                    sale.save()


                    total_amount = 0


                    # =========================================
                    # معالجة المنتجات
                    # =========================================

                    for form in valid_items:

                        medicine = form.cleaned_data[
                            "medicine"
                        ]

                        quantity = form.cleaned_data[
                            "quantity"
                        ]

                        selling_price = form.cleaned_data[
                            "selling_price"
                        ]


                        # -------------------------------------
                        # إعادة قراءة الدواء من قاعدة البيانات
                        # -------------------------------------

                        medicine = medicine.__class__.objects.select_for_update().get(
                            pk=medicine.pk
                        )


                        # -------------------------------------
                        # التحقق من المخزون
                        # -------------------------------------

                        if medicine.quantity < quantity:

                            raise ValueError(
                                f"الكمية المطلوبة من "
                                f"{medicine.name} غير متوفرة. "
                                f"المتاح حاليًا: "
                                f"{medicine.quantity}"
                            )


                        # -------------------------------------
                        # حساب إجمالي المنتج
                        # -------------------------------------

                        subtotal = (
                            quantity *
                            selling_price
                        )


                        # -------------------------------------
                        # إنشاء تفاصيل الفاتورة
                        # -------------------------------------

                        item = form.save(
                            commit=False
                        )

                        item.sale = sale

                        item.medicine = medicine

                        item.quantity = quantity

                        item.selling_price = selling_price

                        item.subtotal = subtotal

                        item.save()


                        # -------------------------------------
                        # حفظ الكمية السابقة قبل خصم البيع
                        # -------------------------------------

                        previous_quantity = medicine.quantity

                        # -------------------------------------
                        # خصم الكمية من المخزون
                        # -------------------------------------

                        medicine.quantity -= quantity


                        # -------------------------------------
                        # تحديث حالة الدواء
                        # -------------------------------------

                        if medicine.quantity <= 0:

                            medicine.quantity = 0

                            medicine.status = "unavailable"

                        else:

                            medicine.status = "available"


                        medicine.save(
                            update_fields=[
                                "quantity",
                                "status",
                                "updated_at",
                            ]
                        )


                        # -------------------------------------
                        # إضافة إجمالي المنتج
                        # -------------------------------------

                        total_amount += subtotal


                    # =========================================
                    # تحديث إجمالي الفاتورة
                    # =========================================

                    sale.total_amount = total_amount

                    sale.save(
                        update_fields=[
                            "total_amount",
                            "updated_at",
                        ]
                    )


                # =========================================
                # إشعار إنشاء فاتورة بيع
                # المدير + الصيدلي
                # =========================================

                notify_admins_and_pharmacists(

                    title="فاتورة بيع جديدة",

                    message=(
                        f"تم إنشاء فاتورة بيع جديدة "
                        f"رقم #{sale.id} "
                        f"بواسطة {request.user.full_name}."
                    ),

                    notification_type="order"
                )


                # =========================================
                # إشعارات المخزون بعد البيع
                # =========================================
                # يتم إرسال الإشعار فقط عند انتقال الدواء
                # من مستوى طبيعي إلى مستوى منخفض/منعدم.
                # حتى لا يتكرر الإشعار مع كل عملية بيع
                # بينما الدواء ما زال أصلًا في حالة منخفضة.

                for form in valid_items:

                    medicine = form.cleaned_data[
                        "medicine"
                    ]

                    medicine = medicine.__class__.objects.get(
                        pk=medicine.pk
                    )

                    # -----------------------------------------
                    # الحصول على الكمية السابقة من تفاصيل البيع
                    # -----------------------------------------

                    quantity_sold = form.cleaned_data[
                        "quantity"
                    ]

                    previous_quantity = (
                        medicine.quantity + quantity_sold
                    )

                    # -----------------------------------------
                    # نفاد المخزون
                    # -----------------------------------------

                    if (
                        medicine.quantity == 0
                        and previous_quantity > 0
                    ):

                        notify_admins_and_pharmacists(

                            title="نفاد المخزون",

                            message=(
                                f"نفد مخزون الدواء "
                                f"{medicine.name} "
                                f"بعد إنشاء فاتورة البيع "
                                f"#{sale.id}."
                            ),

                            notification_type="stock"
                        )

                    # -----------------------------------------
                    # انخفاض المخزون
                    # -----------------------------------------
                    # لا نرسل الإشعار إلا إذا كان المخزون
                    # قبل البيع أعلى من الحد الأدنى وأصبح
                    # بعد البيع عند الحد الأدنى أو أقل.

                    elif (
                        previous_quantity
                        > medicine.minimum_stock
                        and medicine.quantity
                        <= medicine.minimum_stock
                    ):

                        notify_admins_and_pharmacists(

                            title="انخفاض المخزون",

                            message=(
                                f"انخفض مخزون الدواء "
                                f"{medicine.name} "
                                f"إلى {medicine.quantity} "
                                f"وهو عند أو أقل من الحد الأدنى "
                                f"للمخزون."
                            ),

                            notification_type="stock"
                        )


                messages.success(
                    request,
                    f"تم إنشاء فاتورة البيع #{sale.id} "
                    f"بنجاح وتحديث المخزون."
                )

                return redirect(
                    "sale_detail",
                    pk=sale.id
                )


            except ValueError as error:

                messages.error(
                    request,
                    str(error)
                )

                return render(
                    request,
                    "sales/sale_form.html",
                    {
                        "sale_form": sale_form,
                        "item_formset": item_formset,
                    }
                )


    else:

        sale_form = SaleForm()

        item_formset = SaleItemFormSet()


    return render(
        request,
        "sales/sale_form.html",
        {
            "sale_form": sale_form,
            "item_formset": item_formset,
        }
    )


# =========================================================
# تفاصيل فاتورة البيع
# =========================================================

@pharmacist_required
def sale_detail(request, pk):

    sale = get_object_or_404(
        Sale.objects.select_related(
            "customer",
            "cashier"
        ).prefetch_related(
            "items__medicine"
        ),
        pk=pk
    )

    return render(
        request,
        "sales/sale_detail.html",
        {
            "sale": sale,
        }
    )