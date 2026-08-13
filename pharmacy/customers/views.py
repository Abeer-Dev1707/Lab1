from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import (
    Customer,
    CustomerOrder,
    CustomerOrderItem,
)

from .forms import (
    CustomerForm,
    CustomerOrderForm,
    CustomerOrderItemFormSet,
)

from accounts.decorators import pharmacist_required

from medicines.models import Medicine
from sales.models import Sale, SaleItem
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.db import transaction

from .models import Customer, CustomerOrder

from django.db import transaction
from django.utils import timezone

from .models import (
    Customer,
    CustomerOrder,
    CustomerOrderItem,
)

from medicines.models import Medicine

from sales.models import Sale, SaleItem

from sales.models import Sale



# =========================================================
# قائمة العملاء
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def customer_list(request):

    search = request.GET.get("search", "")

    customers = Customer.objects.all()

    if search:

        customers = customers.filter(

            Q(full_name__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search) |
            Q(address__icontains=search)

        )

    paginator = Paginator(customers, 10)

    page_number = request.GET.get("page")

    customers = paginator.get_page(page_number)

    return render(
        request,
        "customers/customer_list.html",
        {
            "customers": customers,
            "search": search,
        }
    )


# =========================================================
# إضافة عميل
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def customer_create(request):

    if request.method == "POST":

        form = CustomerForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "تمت إضافة العميل بنجاح."
            )

            return redirect("customer_list")

    else:

        form = CustomerForm()

    return render(
        request,
        "customers/customer_form.html",
        {
            "form": form,
            "page_title": "إضافة عميل",
        }
    )


# =========================================================
# تعديل العميل
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def customer_update(request, pk):

    customer = get_object_or_404(
        Customer,
        pk=pk
    )

    if request.method == "POST":

        form = CustomerForm(
            request.POST,
            instance=customer
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "تم تعديل بيانات العميل بنجاح."
            )

            return redirect("customer_list")

    else:

        form = CustomerForm(
            instance=customer
        )

    return render(
        request,
        "customers/customer_form.html",
        {
            "form": form,
            "page_title": "تعديل العميل",
        }
    )


# =========================================================
# حذف العميل
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def customer_delete(request, pk):

    customer = get_object_or_404(
        Customer,
        pk=pk
    )

    if request.method == "POST":

        customer.delete()

        messages.success(
            request,
            "تم حذف العميل بنجاح."
        )

        return redirect("customer_list")

    return render(
        request,
        "customers/customer_delete.html",
        {
            "customer": customer,
        }
    )


# =========================================================
# منتجات الصيدلية
# العميل فقط
# =========================================================

@login_required(login_url="login")
def customer_products(request):

    # التأكد أن المستخدم عميل
    if request.user.role != "customer":

        messages.error(
            request,
            "غير مسموح لك بالوصول إلى هذه الصفحة."
        )

        return redirect("dashboard")


    # تاريخ اليوم
    today = timezone.now().date()


    # المنتجات المتاحة وغير المنتهية فقط
    medicines = Medicine.objects.filter(
        status="available",
        expiry_date__gte=today
    ).select_related(
        "category",
        "product_type"
    ).order_by(
        "name"
    )


    return render(
        request,
        "customers/customer_products.html",
        {
            "medicines": medicines,
        }
    )

# =========================================================
# إنشاء طلب للعميل
# العميل فقط
# =========================================================

@login_required(login_url="login")
def customer_order_create(request):

    # -----------------------------------------------------
    # التأكد أن المستخدم عميل
    # -----------------------------------------------------

    if request.user.role != "customer":

        messages.error(
            request,
            "غير مسموح لك بالوصول إلى هذه الصفحة."
        )

        return redirect("dashboard")


    # -----------------------------------------------------
    # الحصول على ملف العميل
    # -----------------------------------------------------

    customer = get_object_or_404(
        Customer,
        user=request.user
    )


    # -----------------------------------------------------
    # الدواء المحدد من صفحة المنتجات
    # -----------------------------------------------------

    selected_medicine = None

    medicine_id = request.GET.get("medicine")

    if medicine_id:

        selected_medicine = get_object_or_404(
            Medicine,
            pk=medicine_id,
            status="available",
            expiry_date__gte=timezone.now().date()
        )


    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        order_form = CustomerOrderForm(
            request.POST
        )

        item_formset = CustomerOrderItemFormSet(
            request.POST
        )


        if (
            order_form.is_valid()
            and item_formset.is_valid()
        ):

            # ---------------------------------------------
            # المنتجات الصحيحة
            # ---------------------------------------------

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

                    valid_items.append(form)


            # ---------------------------------------------
            # يجب وجود منتج
            # ---------------------------------------------

            if not valid_items:

                messages.error(
                    request,
                    "يجب إضافة دواء واحد على الأقل إلى الطلب."
                )

                return render(
                    request,
                    "customers/customer_order_form.html",
                    {
                        "order_form": order_form,
                        "item_formset": item_formset,
                    }
                )


            try:

                with transaction.atomic():

                    # =====================================
                    # إنشاء الطلب
                    # =====================================

                    order = order_form.save(
                        commit=False
                    )

                    order.customer = customer

                    order.status = "pending"

                    order.total_amount = 0

                    order.save()


                    total_amount = 0


                    # =====================================
                    # معالجة المنتجات
                    # =====================================

                    for form in valid_items:

                        medicine = form.cleaned_data[
                            "medicine"
                        ]

                        quantity = form.cleaned_data[
                            "quantity"
                        ]


                        # ---------------------------------
                        # إعادة قراءة الدواء
                        # ---------------------------------

                        medicine = Medicine.objects.get(
                            pk=medicine.pk
                        )


                        # ---------------------------------
                        # التحقق من الصلاحية
                        # ---------------------------------

                        today = timezone.now().date()

                        if medicine.expiry_date < today:

                            raise ValueError(
                                f"الدواء {medicine.name} "
                                f"منتهي الصلاحية ولا يمكن طلبه."
                            )


                        # ---------------------------------
                        # التحقق من التوفر
                        # ---------------------------------

                        if medicine.status != "available":

                            raise ValueError(
                                f"الدواء {medicine.name} "
                                f"غير متوفر حاليًا."
                            )


                        # ---------------------------------
                        # التحقق من المخزون
                        # ---------------------------------

                        if medicine.quantity < quantity:

                            raise ValueError(
                                f"الكمية المطلوبة من "
                                f"{medicine.name} غير متوفرة. "
                                f"المتاح حاليًا: "
                                f"{medicine.quantity}"
                            )


                        # ---------------------------------
                        # السعر من قاعدة البيانات
                        # ---------------------------------

                        selling_price = medicine.selling_price


                        # ---------------------------------
                        # الإجمالي
                        # ---------------------------------

                        subtotal = (
                            quantity *
                            selling_price
                        )


                        # ---------------------------------
                        # إنشاء المنتج داخل الطلب
                        # ---------------------------------

                        CustomerOrderItem.objects.create(

                            order=order,

                            medicine=medicine,

                            quantity=quantity,

                            selling_price=selling_price,

                            subtotal=subtotal,

                        )


                        total_amount += subtotal


                    # =====================================
                    # تحديث إجمالي الطلب
                    # =====================================

                    order.total_amount = total_amount

                    order.save(
                        update_fields=[
                            "total_amount",
                            "updated_at",
                        ]
                    )


                messages.success(
                    request,
                    f"تم إرسال الطلب #{order.id} "
                    f"بنجاح، وهو الآن قيد المراجعة."
                )


                return redirect(
                    "customer_order_detail",
                    pk=order.id
                )


            except ValueError as error:

                messages.error(
                    request,
                    str(error)
                )


    # =====================================================
    # GET
    # =====================================================

    else:

        order_form = CustomerOrderForm()

        item_formset = CustomerOrderItemFormSet()


        # ---------------------------------------------
        # إذا اختار العميل دواء من صفحة المنتجات
        # ---------------------------------------------

        if selected_medicine:

            first_form = item_formset.forms[0]

            first_form.initial["medicine"] = (
                selected_medicine.pk
            )


    return render(
        request,
        "customers/customer_order_form.html",
        {
            "order_form": order_form,
            "item_formset": item_formset,
            "selected_medicine": selected_medicine,
        }
    )


# =========================================================
# تفاصيل طلب العميل
# العميل يرى طلباته فقط
# =========================================================

@login_required(login_url="login")
def customer_order_detail(request, pk):

    if request.user.role != "customer":

        messages.error(
            request,
            "غير مسموح لك بالوصول إلى هذه الصفحة."
        )

        return redirect("dashboard")


    customer = get_object_or_404(
        Customer,
        user=request.user
    )


    order = get_object_or_404(
        CustomerOrder.objects.prefetch_related(
            "items__medicine"
        ),
        pk=pk,
        customer=customer
    )


    # الفاتورة المرتبطة بهذا الطلب
    sale = Sale.objects.filter(
        customer_order=order,
        customer=customer
    ).first()


    return render(
        request,
        "customers/customer_order_detail.html",
        {
            "order": order,
            "sale": sale,
        }
    )

# =========================================================
# تفاصيل فاتورة العميل
# العميل يرى فواتيره الخاصة فقط
# =========================================================

@login_required(login_url="login")
def customer_sale_detail(request, pk):

    # -----------------------------------------------------
    # التأكد أن المستخدم عميل
    # -----------------------------------------------------

    if request.user.role != "customer":

        messages.error(
            request,
            "غير مسموح لك بالوصول إلى هذه الصفحة."
        )

        return redirect("dashboard")


    # -----------------------------------------------------
    # الحصول على العميل المرتبط بالحساب
    # -----------------------------------------------------

    customer = get_object_or_404(
        Customer,
        user=request.user
    )


    # -----------------------------------------------------
    # الحصول على الفاتورة الخاصة بهذا العميل فقط
    # -----------------------------------------------------

    sale = get_object_or_404(
        Sale.objects.select_related(
            "customer",
            "customer_order"
        ).prefetch_related(
            "items__medicine"
        ),
        pk=pk,
        customer=customer
    )


    return render(
        request,
        "customers/customer_sale_detail.html",
        {
            "sale": sale,
        }
    )

# =========================================================
# طلبات العميل
# العميل يرى طلباته فقط
# =========================================================

@login_required(login_url="login")
def customer_orders(request):

    # -----------------------------------------------------
    # التأكد أن المستخدم عميل
    # -----------------------------------------------------

    if request.user.role != "customer":

        messages.error(
            request,
            "غير مسموح لك بالوصول إلى هذه الصفحة."
        )

        return redirect("dashboard")


    # -----------------------------------------------------
    # الحصول على ملف العميل
    # -----------------------------------------------------

    customer = get_object_or_404(
        Customer,
        user=request.user
    )


    # -----------------------------------------------------
    # جلب طلبات هذا العميل فقط
    # -----------------------------------------------------

    orders = CustomerOrder.objects.filter(
        customer=customer
    ).prefetch_related(
        "items__medicine"
    ).order_by(
        "-created_at"
    )


    return render(
        request,
        "customers/customer_orders.html",
        {
            "orders": orders,
        }
    )


# =========================================================
# إدارة طلبات العملاء
#
# المدير + الصيدلي فقط
# =========================================================

@pharmacist_required
def customer_order_manage(request):

    orders = CustomerOrder.objects.select_related(
        "customer"
    ).prefetch_related(
        "items__medicine"
    ).all()

    return render(
        request,
        "customers/customer_order_manage.html",
        {
            "orders": orders,
        }
    )

# =========================================================
# تفاصيل طلب العميل
#
# المدير + الصيدلي فقط
# =========================================================

@pharmacist_required
def customer_order_manage_detail(request, pk):

    order = get_object_or_404(
        CustomerOrder.objects.select_related(
            "customer"
        ).prefetch_related(
            "items__medicine"
        ),
        pk=pk
    )

    return render(
        request,
        "customers/customer_order_manage_detail.html",
        {
            "order": order,
        }
    )

# =========================================================
# الموافقة على طلب العميل
#
# المدير + الصيدلي
# =========================================================
# =========================================================
# الموافقة على طلب العميل
#
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def customer_order_approve(request, pk):

    # -----------------------------------------------------
    # يجب أن تكون العملية POST
    # -----------------------------------------------------

    if request.method != "POST":

        return redirect(
            "customer_order_manage_detail",
            pk=pk
        )


    try:

        with transaction.atomic():

            # =============================================
            # قفل الطلب أثناء المعالجة
            # =============================================

            order = CustomerOrder.objects.select_for_update().get(
                pk=pk
            )


            # =============================================
            # منع معالجة الطلب أكثر من مرة
            # =============================================

            if order.status != "pending":

                messages.error(
                    request,
                    "لا يمكن معالجة هذا الطلب لأنه تمت معالجته مسبقًا."
                )

                return redirect(
                    "customer_order_manage_detail",
                    pk=order.id
                )


            # =============================================
            # جلب المنتجات
            # =============================================

            items = list(
                order.items.select_related(
                    "medicine"
                )
            )


            # =============================================
            # التأكد من وجود منتجات
            # =============================================

            if not items:

                messages.error(
                    request,
                    "لا يمكن الموافقة على طلب لا يحتوي على منتجات."
                )

                return redirect(
                    "customer_order_manage_detail",
                    pk=order.id
                )


            today = timezone.now().date()


            # =============================================
            # التحقق من جميع المنتجات أولًا
            # =============================================

            medicines = []


            for item in items:

                medicine = Medicine.objects.select_for_update().get(
                    pk=item.medicine_id
                )


                # -----------------------------------------
                # التحقق من الصلاحية
                # -----------------------------------------

                if medicine.expiry_date < today:

                    raise ValueError(
                        f"الدواء {medicine.name} "
                        f"منتهي الصلاحية ولا يمكن الموافقة على الطلب."
                    )


                # -----------------------------------------
                # التحقق من الحالة
                # -----------------------------------------

                if medicine.status != "available":

                    raise ValueError(
                        f"الدواء {medicine.name} "
                        f"غير متوفر حاليًا."
                    )


                # -----------------------------------------
                # التحقق من الكمية
                # -----------------------------------------

                if medicine.quantity < item.quantity:

                    raise ValueError(
                        f"الكمية المطلوبة من "
                        f"{medicine.name} غير متوفرة. "
                        f"المتاح حاليًا: "
                        f"{medicine.quantity}"
                    )


                medicines.append(
                    (medicine, item.quantity)
                )


            # =============================================
            # خصم المخزون
            # =============================================

            for medicine, quantity in medicines:

                medicine.quantity -= quantity


                # -----------------------------------------
                # تحديث حالة الدواء
                # -----------------------------------------

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


            # =============================================
            # إنشاء فاتورة البيع
            # =============================================

            sale = Sale.objects.create(

                customer=order.customer,

                customer_order=order,

                cashier=request.user,

                status="completed",

                total_amount=order.total_amount,

                notes=order.notes

            )


            # =============================================
            # إنشاء تفاصيل الفاتورة
            # =============================================

            for item in items:

                SaleItem.objects.create(

                    sale=sale,

                    medicine=item.medicine,

                    quantity=item.quantity,

                    selling_price=item.selling_price,

                    subtotal=item.subtotal

                )


            # =============================================
            # تحديث حالة الطلب
            # =============================================

            order.status = "completed"

            order.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )


        # =============================================
        # رسالة النجاح
        # =============================================

        messages.success(
            request,
            f"تمت الموافقة على الطلب #{order.id} "
            f"وإنشاء فاتورة البيع #{sale.id} "
            f"وتحديث المخزون بنجاح."
        )


    except CustomerOrder.DoesNotExist:

        messages.error(
            request,
            "الطلب غير موجود."
        )

        return redirect(
            "customer_order_manage"
        )


    except ValueError as error:

        messages.error(
            request,
            str(error)
        )


    return redirect(
        "customer_order_manage_detail",
        pk=pk
    )


# =========================================================
# رفض طلب العميل
#
# المدير + الصيدلي
# =========================================================

@pharmacist_required
def customer_order_reject(request, pk):

    if request.method != "POST":

        return redirect(
            "customer_order_manage_detail",
            pk=pk
        )


    order = get_object_or_404(
        CustomerOrder,
        pk=pk
    )


    # =============================================
    # لا يمكن رفض طلب تمت معالجته
    # =============================================

    if order.status != "pending":

        messages.error(
            request,
            "لا يمكن رفض هذا الطلب لأنه تمت معالجته مسبقًا."
        )

        return redirect(
            "customer_order_manage_detail",
            pk=pk
        )


    # =============================================
    # تغيير الحالة فقط
    # لا يتم لمس المخزون
    # =============================================

    order.status = "rejected"

    order.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )


    messages.success(
        request,
        f"تم رفض الطلب #{order.id}."
    )


    return redirect(
        "customer_order_manage_detail",
        pk=pk
    )