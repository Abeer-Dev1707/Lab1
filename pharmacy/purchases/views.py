from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from decimal import Decimal, InvalidOperation

from .forms import (
    PurchaseOrderForm,
    PurchaseItemFormSet,
)

from .models import PurchaseOrder


# =========================================================
# قائمة طلبات التوريد
# المدير + الصيدلي + المورد
# =========================================================

@login_required(login_url="login")
def purchase_list(request):

    # =====================================================
    # المورد يرى طلباته فقط
    # =====================================================

    if request.user.role == "supplier":

        orders = PurchaseOrder.objects.filter(
            supplier__user=request.user
        ).select_related(
            "supplier"
        ).prefetch_related(
            "items__medicine"
        ).order_by(
            "-created_at"
        )

    # =====================================================
    # المدير والصيدلي يرون جميع الطلبات
    # =====================================================

    elif request.user.role in ["admin", "pharmacist"]:

        orders = PurchaseOrder.objects.select_related(
            "supplier"
        ).prefetch_related(
            "items__medicine"
        ).all().order_by(
            "-created_at"
        )

    # =====================================================
    # باقي المستخدمين
    # =====================================================

    else:

        messages.error(
            request,
            "🚫 غير مسموح لك بالوصول إلى طلبات التوريد."
        )

        return redirect("dashboard")

    return render(
        request,
        "purchases/purchase_list.html",
        {
            "orders": orders,
        }
    )


# =========================================================
# إنشاء طلب توريد
# المدير + الصيدلي
#
# الصيدلية تحدد:
#   - المورد
#   - الدواء
#   - الكمية
#
# المورد يحدد سعر الشراء لاحقًا.
# =========================================================

@login_required(login_url="login")
def purchase_create(request):

    # -----------------------------------------------------
    # المدير والصيدلي فقط
    # -----------------------------------------------------

    if request.user.role not in ["admin", "pharmacist"]:

        messages.error(
            request,
            "🚫 غير مسموح لك بإنشاء طلب توريد."
        )

        return redirect("dashboard")

    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    if request.method == "POST":

        order_form = PurchaseOrderForm(
            request.POST
        )

        item_formset = PurchaseItemFormSet(
            request.POST
        )

        # -------------------------------------------------
        # التحقق من الطلب والمنتجات
        # -------------------------------------------------

        if (
            order_form.is_valid()
            and item_formset.is_valid()
        ):

            # ---------------------------------------------
            # إنشاء الطلب
            # ---------------------------------------------

            order = order_form.save()

            # ---------------------------------------------
            # ربط المنتجات بالطلب
            # ---------------------------------------------

            item_formset.instance = order

            items = item_formset.save(
                commit=False
            )

            # ---------------------------------------------
            # التأكد أن كل منتج يبدأ بدون سعر
            #
            # السعر سيحدده المورد لاحقًا.
            # ---------------------------------------------

            for item in items:

                item.purchase_price = None

                item.save()

            # ---------------------------------------------
            # حذف العناصر التي تم تحديدها للحذف
            # ---------------------------------------------

            for item in item_formset.deleted_objects:

                if item.pk:
                    item.delete()

            messages.success(
                request,
                "تم إنشاء طلب التوريد بنجاح، وتم إرساله إلى المورد لتحديد السعر."
            )

            return redirect(
                "purchase_list"
            )

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    else:

        order_form = PurchaseOrderForm()

        item_formset = PurchaseItemFormSet()

    return render(
        request,
        "purchases/purchase_form.html",
        {
            "order_form": order_form,
            "item_formset": item_formset,
        }
    )


# =========================================================
# تفاصيل طلب التوريد
# المدير + الصيدلي + المورد صاحب الطلب
# =========================================================

@login_required(login_url="login")
def purchase_detail(request, pk):

    order = get_object_or_404(
        PurchaseOrder.objects.select_related(
            "supplier"
        ).prefetch_related(
            "items__medicine"
        ),
        pk=pk
    )

    # =====================================================
    # المورد يرى طلباته فقط
    # =====================================================

    if request.user.role == "supplier":

        if order.supplier.user != request.user:

            messages.error(
                request,
                "🚫 غير مسموح لك بالوصول إلى هذا الطلب."
            )

            return redirect(
                "dashboard"
            )

    # =====================================================
    # المستخدمون الآخرون المسموح لهم
    # =====================================================

    elif request.user.role not in [
        "admin",
        "pharmacist"
    ]:

        messages.error(
            request,
            "🚫 غير مسموح لك بالوصول إلى هذه الصفحة."
        )

        return redirect(
            "dashboard"
        )

    return render(
        request,
        "purchases/purchase_detail.html",
        {
            "order": order,
        }
    )


# =========================================================
# طلبات التوريد للمورد
# المورد فقط
# =========================================================

@login_required(login_url="login")
def supplier_orders(request):

    # -----------------------------------------------------
    # المورد فقط
    # -----------------------------------------------------

    if request.user.role != "supplier":

        messages.error(
            request,
            "🚫 غير مسموح لك بالوصول إلى هذه الصفحة."
        )

        return redirect(
            "dashboard"
        )

    orders = PurchaseOrder.objects.filter(
        supplier__user=request.user
    ).select_related(
        "supplier"
    ).prefetch_related(
        "items__medicine"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "purchases/supplier_orders.html",
        {
            "orders": orders,
        }
    )


# =========================================================
# موافقة المورد على طلب التوريد
#
# المورد يحدد سعر كل منتج ثم يوافق.
#
# المورد صاحب الطلب فقط
# =========================================================

@login_required(login_url="login")
def supplier_approve_order(request, pk):

    # =====================================================
    # المورد فقط
    # =====================================================

    if request.user.role != "supplier":

        messages.error(
            request,
            "🚫 غير مسموح لك بتنفيذ هذا الإجراء."
        )

        return redirect(
            "dashboard"
        )

    # =====================================================
    # الحصول على الطلب
    # =====================================================

    order = get_object_or_404(
        PurchaseOrder.objects.prefetch_related(
            "items__medicine"
        ),
        pk=pk
    )

    # =====================================================
    # التأكد أن الطلب تابع لهذا المورد
    # =====================================================

    if order.supplier.user != request.user:

        messages.error(
            request,
            "🚫 غير مسموح لك بتعديل هذا الطلب."
        )

        return redirect(
            "supplier_orders"
        )

    # =====================================================
    # الموافقة يجب أن تكون POST
    # =====================================================

    if request.method != "POST":

        messages.warning(
            request,
            "⚠️ يجب إرسال نموذج الموافقة بالطريقة الصحيحة."
        )

        return redirect(
            "purchase_detail",
            pk=order.id
        )

    # =====================================================
    # لا يمكن الموافقة إلا على طلب قيد المراجعة
    # =====================================================

    if order.status != "pending":

        messages.warning(
            request,
            "⚠️ لا يمكن تغيير حالة هذا الطلب."
        )

        return redirect(
            "purchase_detail",
            pk=order.id
        )

    # =====================================================
    # التأكد من وجود منتجات في الطلب
    # =====================================================

    items = list(
        order.items.all()
    )

    if not items:

        messages.error(
            request,
            "🚫 لا يمكن الموافقة على طلب لا يحتوي على منتجات."
        )

        return redirect(
            "purchase_detail",
            pk=order.id
        )

    # =====================================================
    # قراءة الأسعار التي أدخلها المورد
    #
    # اسم الحقل المتوقع:
    #
    # purchase_price_<item_id>
    #
    # مثال:
    #
    # purchase_price_5
    # =====================================================

    prices = {}

    for item in items:

        field_name = f"purchase_price_{item.id}"

        price_value = request.POST.get(
            field_name,
            ""
        ).strip()

        # -------------------------------------------------
        # السعر فارغ
        # -------------------------------------------------

        if not price_value:

            messages.error(
                request,
                f"🚫 يرجى تحديد سعر الشراء للدواء: {item.medicine.name}."
            )

            return redirect(
                "purchase_detail",
                pk=order.id
            )

        # -------------------------------------------------
        # تحويل السعر إلى Decimal
        # -------------------------------------------------

        try:

            price = Decimal(
                price_value
            )

        except (InvalidOperation, ValueError):

            messages.error(
                request,
                f"🚫 سعر الدواء {item.medicine.name} غير صحيح."
            )

            return redirect(
                "purchase_detail",
                pk=order.id
            )

        # -------------------------------------------------
        # السعر يجب أن يكون أكبر من صفر
        # -------------------------------------------------

        if price <= 0:

            messages.error(
                request,
                f"🚫 يجب أن يكون سعر {item.medicine.name} أكبر من صفر."
            )

            return redirect(
                "purchase_detail",
                pk=order.id
            )

        # -------------------------------------------------
        # حفظ السعر في الذاكرة مؤقتًا
        # -------------------------------------------------

        prices[item.id] = price

    # =====================================================
    # حفظ الأسعار وتحويل الطلب إلى approved
    # =====================================================

    with transaction.atomic():

        for item in items:

            item.purchase_price = prices[item.id]

            item.save(
                update_fields=[
                    "purchase_price"
                ]
            )

        order.status = "approved"

        order.save(
            update_fields=[
                "status",
                "updated_at"
            ]
        )

    # =====================================================
    # رسالة نجاح
    # =====================================================

    messages.success(
        request,
        "✅ تمت الموافقة على طلب التوريد وتسجيل أسعار المنتجات بنجاح."
    )

    return redirect(
        "purchase_detail",
        pk=order.id
    )


# =========================================================
# رفض المورد لطلب التوريد
# المورد صاحب الطلب فقط
# =========================================================

@login_required(login_url="login")
def supplier_reject_order(request, pk):

    # =====================================================
    # المورد فقط
    # =====================================================

    if request.user.role != "supplier":

        messages.error(
            request,
            "🚫 غير مسموح لك بتنفيذ هذا الإجراء."
        )

        return redirect(
            "dashboard"
        )

    # =====================================================
    # الحصول على الطلب
    # =====================================================

    order = get_object_or_404(
        PurchaseOrder,
        pk=pk
    )

    # =====================================================
    # التأكد أن الطلب تابع لهذا المورد
    # =====================================================

    if order.supplier.user != request.user:

        messages.error(
            request,
            "🚫 غير مسموح لك بتعديل هذا الطلب."
        )

        return redirect(
            "supplier_orders"
        )

    # =====================================================
    # الرفض يجب أن يكون POST
    # =====================================================

    if request.method != "POST":

        messages.warning(
            request,
            "⚠️ يجب إرسال نموذج الرفض بالطريقة الصحيحة."
        )

        return redirect(
            "purchase_detail",
            pk=order.id
        )

    # =====================================================
    # لا يمكن رفض إلا طلب قيد المراجعة
    # =====================================================

    if order.status != "pending":

        messages.warning(
            request,
            "⚠️ لا يمكن تغيير حالة هذا الطلب."
        )

        return redirect(
            "purchase_detail",
            pk=order.id
        )

    # =====================================================
    # تغيير الحالة إلى مرفوض
    # =====================================================

    order.status = "rejected"

    order.save(
        update_fields=[
            "status",
            "updated_at"
        ]
    )

    messages.warning(
        request,
        "تم رفض طلب التوريد."
    )

    return redirect(
        "purchase_detail",
        pk=order.id
    )


# =========================================================
# تأكيد استلام طلب التوريد
#
# المدير + الصيدلي
#
# عند الاستلام:
#
# PurchaseItem.quantity
#        ↓
# Medicine.quantity += الكمية
#
# ثم:
#
# order.status = completed
# =========================================================

@login_required(login_url="login")
def purchase_receive(request, pk):

    # =====================================================
    # المدير والصيدلي فقط
    # =====================================================

    if request.user.role not in [
        "admin",
        "pharmacist"
    ]:

        messages.error(
            request,
            "🚫 غير مسموح لك بتأكيد استلام التوريد."
        )

        return redirect(
            "dashboard"
        )

    # =====================================================
    # يجب أن يكون الطلب موجودًا
    # =====================================================

    order = get_object_or_404(
        PurchaseOrder.objects.prefetch_related(
            "items__medicine"
        ),
        pk=pk
    )

    # =====================================================
    # يجب أن تكون حالة الطلب تمت الموافقة
    # =====================================================

    if order.status != "approved":

        messages.warning(
            request,
            "⚠️ لا يمكن استلام هذا الطلب لأن حالته ليست تمت الموافقة."
        )

        return redirect(
            "purchase_detail",
            pk=order.id
        )

    # =====================================================
    # تنفيذ الاستلام يجب أن يكون POST
    # =====================================================

    if request.method != "POST":

        messages.warning(
            request,
            "⚠️ يجب تأكيد الاستلام بالطريقة الصحيحة."
        )

        return redirect(
            "purchase_detail",
            pk=order.id
        )

    # =====================================================
    # تنفيذ عملية الاستلام داخل Transaction
    # =====================================================

    with transaction.atomic():

        # -------------------------------------------------
        # تحديث كمية كل دواء
        # -------------------------------------------------

        for item in order.items.all():

            medicine = item.medicine

            medicine.quantity += item.quantity

            # ---------------------------------------------
            # إذا أصبحت الكمية أكبر من صفر
            # نجعل الدواء متوفرًا
            # ---------------------------------------------

            if medicine.quantity > 0:

                medicine.status = "available"

            medicine.save(
                update_fields=[
                    "quantity",
                    "status",
                    "updated_at",
                ]
            )

        # -------------------------------------------------
        # تحويل حالة الطلب إلى مكتمل
        # -------------------------------------------------

        order.status = "completed"

        order.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

    # =====================================================
    # رسالة النجاح
    # =====================================================

    messages.success(
        request,
        "✅ تم استلام طلب التوريد بنجاح وتم تحديث المخزون."
    )

    return redirect(
        "purchase_detail",
        pk=order.id
    )