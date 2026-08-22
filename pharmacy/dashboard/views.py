from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth

from categories.models import Category
from accounts.models import User
from medicines.models import Medicine
from customers.models import Customer, CustomerOrder
from suppliers.models import Supplier
from purchases.models import PurchaseOrder
from sales.models import Sale
from django.contrib.auth import update_session_auth_hash


# =========================================================
# تسجيل الدخول
# =========================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        # ==========================================
        # البحث عن الحساب أولًا
        # ==========================================

        try:

            user = User.objects.get(
                username=username
            )

        except User.DoesNotExist:

            messages.error(
                request,
                "اسم المستخدم أو كلمة المرور غير صحيحة."
            )

            return render(
                request,
                "dashboard/login.html"
            )

        # ==========================================
        # التحقق من حالة الحساب
        # ==========================================

        if user.account_status == "pending":

            messages.warning(
                request,
                "⏳ حسابك قيد المراجعة. "
                "يرجى انتظار موافقة المدير قبل تسجيل الدخول."
            )

            return render(
                request,
                "dashboard/login.html"
            )

        if user.account_status == "rejected":

            messages.error(
                request,
                "🚫 تم رفض طلب إنشاء حسابك. "
                "يرجى التواصل مع إدارة الصيدلية."
            )

            return render(
                request,
                "dashboard/login.html"
            )

        # ==========================================
        # التحقق من اسم المستخدم وكلمة المرور
        # ==========================================

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # ======================================
            # التحقق من أن الحساب فعال
            # ======================================

            if not user.is_active:

                messages.error(
                    request,
                    "🚫 هذا الحساب غير نشط حاليًا."
                )

                return render(
                    request,
                    "dashboard/login.html"
                )

            # ======================================
            # التحقق من أن الحساب مقبول
            # ======================================

            if user.account_status != "approved":

                messages.warning(
                    request,
                    "⏳ لا يمكنك الدخول قبل الموافقة على حسابك."
                )

                return render(
                    request,
                    "dashboard/login.html"
                )

            # ======================================
            # تسجيل الدخول
            # ======================================

            login(
                request,
                user
            )

            messages.success(
                request,
                f"مرحباً {user.username} تم تسجيل الدخول بنجاح."
            )

            return redirect("dashboard")

        else:

            messages.error(
                request,
                "اسم المستخدم أو كلمة المرور غير صحيحة."
            )

    return render(
        request,
        "dashboard/login.html"
    )


# =========================================================
# لوحة التحكم
# تختلف حسب نوع المستخدم
# =========================================================

@login_required(login_url="login")
def home(request):

    # =====================================================
    # العميل
    # =====================================================

    if request.user.role == "customer":

        # ---------------------------------------------
        # الحصول على ملف العميل
        # ---------------------------------------------

        customer = get_object_or_404(
            Customer,
            user=request.user
        )

        # ---------------------------------------------
        # المنتجات المتاحة
        # ---------------------------------------------

        today = timezone.now().date()

        available_medicines = Medicine.objects.filter(
            status="available",
            expiry_date__gte=today
        )

        medicines_count = available_medicines.count()

        # ---------------------------------------------
        # طلبات العميل
        # ---------------------------------------------

        orders = CustomerOrder.objects.filter(
            customer=customer
        ).order_by(
            "-created_at"
        )

        orders_count = orders.count()

        # ---------------------------------------------
        # الطلبات قيد المراجعة
        # ---------------------------------------------

        pending_orders_count = orders.filter(
            status="pending"
        ).count()

        # ---------------------------------------------
        # الطلبات المكتملة
        # ---------------------------------------------

        completed_orders_count = orders.filter(
            status="completed"
        ).count()

        # ---------------------------------------------
        # آخر الطلبات
        # ---------------------------------------------

        latest_orders = orders[:5]

        # ---------------------------------------------
        # لوحة العميل
        # ---------------------------------------------

        return render(
            request,
            "dashboard/customer_dashboard.html",
            {
                "customer": customer,
                "medicines_count": medicines_count,
                "orders_count": orders_count,
                "pending_orders_count": pending_orders_count,
                "completed_orders_count": completed_orders_count,
                "latest_orders": latest_orders,
            }
        )


    # =====================================================
    # المورد
    # =====================================================

    if request.user.role == "supplier":

        # ---------------------------------------------
        # الحصول على ملف المورد
        # ---------------------------------------------

        supplier = get_object_or_404(
            Supplier,
            user=request.user
        )

        # ---------------------------------------------
        # طلبات هذا المورد فقط
        # ---------------------------------------------

        orders = PurchaseOrder.objects.filter(
            supplier=supplier
        ).prefetch_related(
            "items__medicine"
        ).order_by(
            "-created_at"
        )

        # ---------------------------------------------
        # إجمالي الطلبات
        # ---------------------------------------------

        orders_count = orders.count()

        # ---------------------------------------------
        # الطلبات قيد المراجعة
        # ---------------------------------------------

        pending_orders_count = orders.filter(
            status="pending"
        ).count()

        # ---------------------------------------------
        # الطلبات التي تمت الموافقة عليها
        # ---------------------------------------------

        approved_orders_count = orders.filter(
            status="approved"
        ).count()

        # ---------------------------------------------
        # الطلبات المكتملة
        # ---------------------------------------------

        completed_orders_count = orders.filter(
            status="completed"
        ).count()

        # ---------------------------------------------
        # الطلبات المرفوضة
        # ---------------------------------------------

        rejected_orders_count = orders.filter(
            status="rejected"
        ).count()

        # ---------------------------------------------
        # آخر طلبات المورد
        # ---------------------------------------------

        latest_orders = orders[:5]

        # ---------------------------------------------
        # لوحة المورد
        # ---------------------------------------------

        return render(
            request,
            "dashboard/supplier_dashboard.html",
            {
                "supplier": supplier,
                "orders_count": orders_count,
                "pending_orders_count": pending_orders_count,
                "approved_orders_count": approved_orders_count,
                "completed_orders_count": completed_orders_count,
                "rejected_orders_count": rejected_orders_count,
                "latest_orders": latest_orders,
            }
        )


    # =====================================================
    # الصيدلي
    # =====================================================

    if request.user.role == "pharmacist":

        # ---------------------------------------------
        # التاريخ الحالي
        # ---------------------------------------------

        today = timezone.now().date()

        # ---------------------------------------------
        # جميع الأدوية
        # ---------------------------------------------

        medicines = Medicine.objects.all()

        medicines_count = medicines.count()

        # ---------------------------------------------
        # إجمالي كمية المخزون
        # ---------------------------------------------

        total_stock_quantity = (
            medicines.aggregate(
                total=Sum("quantity")
            )["total"] or 0
        )

        # ---------------------------------------------
        # الأدوية منخفضة المخزون
        # ---------------------------------------------

        low_stock_medicines = medicines.filter(
            quantity__gt=0,
            quantity__lte=F("minimum_stock")
        ).order_by(
            "quantity",
            "name"
        )[:5]

        low_stock_count = medicines.filter(
            quantity__gt=0,
            quantity__lte=F("minimum_stock")
        ).count()

        # ---------------------------------------------
        # الأدوية النافدة
        # ---------------------------------------------

        out_of_stock_count = medicines.filter(
            quantity=0
        ).count()

        # ---------------------------------------------
        # طلبات العملاء المعلقة
        # ---------------------------------------------

        pending_customer_orders = CustomerOrder.objects.filter(
            status="pending"
        ).count()

        # ---------------------------------------------
        # طلبات التوريد المعلقة
        # ---------------------------------------------

        pending_purchase_orders = PurchaseOrder.objects.filter(
            status="pending"
        ).count()

        # ---------------------------------------------
        # مبيعات اليوم
        # ---------------------------------------------

        today_sales = Sale.objects.filter(
            created_at__date=today,
            status="completed"
        )

        today_sales_count = today_sales.count()

        today_sales_total = (
            today_sales.aggregate(
                total=Sum("total_amount")
            )["total"] or 0
        )

        # ---------------------------------------------
        # آخر المبيعات
        # ---------------------------------------------

        latest_sales = Sale.objects.select_related(
            "customer"
        ).order_by(
            "-created_at"
        )[:5]

        # ---------------------------------------------
        # لوحة الصيدلي
        # ---------------------------------------------

        return render(
            request,
            "dashboard/pharmacist_dashboard.html",
            {
                "medicines_count": medicines_count,

                "total_stock_quantity": total_stock_quantity,

                "low_stock_medicines": low_stock_medicines,
                "low_stock_count": low_stock_count,
                "out_of_stock_count": out_of_stock_count,

                "pending_customer_orders": pending_customer_orders,
                "pending_purchase_orders": pending_purchase_orders,

                "today_sales_count": today_sales_count,
                "today_sales_total": today_sales_total,

                "latest_sales": latest_sales,
            }
        )


    # =====================================================
    # المدير
    # =====================================================

    categories = Category.objects.all()

    medicines = Medicine.objects.all()
    customers = Customer.objects.all()
    suppliers = Supplier.objects.all()
    sales = Sale.objects.all()

    # -----------------------------------------------------
    # إجمالي الأدوية
    # -----------------------------------------------------

    medicines_count = medicines.count()

    # -----------------------------------------------------
    # إجمالي كمية المخزون
    # -----------------------------------------------------

    total_stock_quantity = (
        medicines.aggregate(
            total=Sum("quantity")
        )["total"] or 0
    )

    # -----------------------------------------------------
    # إجمالي العملاء
    # -----------------------------------------------------

    customers_count = customers.count()

    # -----------------------------------------------------
    # إجمالي الموردين
    # -----------------------------------------------------

    suppliers_count = suppliers.count()

    # -----------------------------------------------------
    # المبيعات المكتملة
    # -----------------------------------------------------

    completed_sales = sales.filter(
        status="completed"
    )

    sales_count = completed_sales.count()

    # -----------------------------------------------------
    # إجمالي قيمة المبيعات المكتملة
    # -----------------------------------------------------

    total_sales_amount = (
        completed_sales.aggregate(
            total=Sum("total_amount")
        )["total"] or 0
    )

    # -----------------------------------------------------
    # الأدوية منخفضة المخزون
    # -----------------------------------------------------

    low_stock_medicines = medicines.filter(
        quantity__gt=0,
        quantity__lte=F("minimum_stock")
    ).order_by(
        "quantity",
        "name"
    )[:5]

    # -----------------------------------------------------
    # عدد الأدوية منخفضة المخزون
    # -----------------------------------------------------

    low_stock_count = medicines.filter(
        quantity__gt=0,
        quantity__lte=F("minimum_stock")
    ).count()

    # -----------------------------------------------------
    # الأدوية النافدة
    # -----------------------------------------------------

    out_of_stock_count = medicines.filter(
        quantity=0
    ).count()

    # -----------------------------------------------------
    # جميع الأدوية النافدة
    # -----------------------------------------------------

    out_of_stock_medicines = medicines.filter(
        quantity=0
    ).order_by(
        "name"
    )[:5]

    # -----------------------------------------------------
    # آخر المبيعات الحقيقية
    # -----------------------------------------------------

    latest_sales = Sale.objects.select_related(
        "customer"
    ).order_by(
        "-created_at"
    )[:5]

    # -----------------------------------------------------
    # مبيعات اليوم
    # -----------------------------------------------------

    today = timezone.now().date()

    today_sales = completed_sales.filter(
        created_at__date=today
    )

    today_sales_count = today_sales.count()

    today_sales_total = (
        today_sales.aggregate(
            total=Sum("total_amount")
        )["total"] or 0
    )

    # -----------------------------------------------------
    # طلبات العملاء
    # -----------------------------------------------------

    pending_customer_orders = CustomerOrder.objects.filter(
        status="pending"
    ).count()

    # -----------------------------------------------------
    # طلبات التوريد
    # -----------------------------------------------------

    pending_purchase_orders = PurchaseOrder.objects.filter(
        status="pending"
    ).count()

    purchase_orders_count = PurchaseOrder.objects.count()

    # -----------------------------------------------------
    # آخر 6 أشهر
    # -----------------------------------------------------

    current_month = today.replace(day=1)

    months = []

    for i in range(5, -1, -1):

        year = current_month.year
        month = current_month.month - i

        while month <= 0:

            month += 12
            year -= 1

        months.append(
            current_month.replace(
                year=year,
                month=month,
                day=1
            )
        )

    # -----------------------------------------------------
    # المبيعات الشهرية الحقيقية
    # -----------------------------------------------------

    monthly_sales_queryset = (
        completed_sales
        .filter(
            created_at__date__gte=months[0],
            created_at__date__lte=today
        )
        .annotate(
            month=TruncMonth("created_at")
        )
        .values("month")
        .annotate(
            total=Sum("total_amount")
        )
        .order_by("month")
    )

    monthly_sales = {}

    for item in monthly_sales_queryset:

        if item["month"]:

            month_date = item["month"].date()

            monthly_sales[month_date] = float(
                item["total"] or 0
            )

    # -----------------------------------------------------
    # أسماء الأشهر
    # -----------------------------------------------------

    month_names = {
        1: "يناير",
        2: "فبراير",
        3: "مارس",
        4: "أبريل",
        5: "مايو",
        6: "يونيو",
        7: "يوليو",
        8: "أغسطس",
        9: "سبتمبر",
        10: "أكتوبر",
        11: "نوفمبر",
        12: "ديسمبر",
    }

    sales_chart_labels = []
    sales_chart_data = []

    for month in months:

        sales_chart_labels.append(
            month_names[month.month]
        )

        sales_chart_data.append(
            monthly_sales.get(
                month,
                0
            )
        )

    # -----------------------------------------------------
    # البيانات التي تصل إلى لوحة المدير
    # -----------------------------------------------------

    context = {

        # ---------------------------------------------
        # البيانات العامة
        # ---------------------------------------------

        "categories": categories,

        "medicines_count": medicines_count,

        "customers_count": customers_count,

        "suppliers_count": suppliers_count,

        "sales_count": sales_count,

        "total_sales_amount": total_sales_amount,

        # ---------------------------------------------
        # المخزون
        # ---------------------------------------------

        "total_stock_quantity": total_stock_quantity,

        "low_stock_medicines": low_stock_medicines,

        "low_stock_count": low_stock_count,

        "out_of_stock_count": out_of_stock_count,

        "out_of_stock_medicines": out_of_stock_medicines,

        # ---------------------------------------------
        # المبيعات
        # ---------------------------------------------

        "latest_sales": latest_sales,

        "today_sales_count": today_sales_count,

        "today_sales_total": today_sales_total,

        # ---------------------------------------------
        # الطلبات
        # ---------------------------------------------

        "pending_customer_orders": pending_customer_orders,

        "pending_purchase_orders": pending_purchase_orders,

        "purchase_orders_count": purchase_orders_count,

        # ---------------------------------------------
        # الرسم البياني
        # ---------------------------------------------

        "sales_chart_labels": sales_chart_labels,

        "sales_chart_data": sales_chart_data,

    }

    # -----------------------------------------------------
    # عرض لوحة المدير
    # -----------------------------------------------------

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )


# =========================================================
# الإعدادات
# المدير فقط
# =========================================================

@login_required(login_url="login")
def settings_view(request):

    # -----------------------------------------------------
    # التحقق من صلاحية المستخدم
    # -----------------------------------------------------

    if request.user.role != "admin":

        return render(
            request,
            "dashboard/dashboard.html",
            {
                "error_message":
                    "غير مسموح لك بالوصول إلى الإعدادات."
            }
        )

    # -----------------------------------------------------
    # عرض صفحة الإعدادات
    # -----------------------------------------------------

    return render(
        request,
        "dashboard/settings.html"
    )

# =========================================================
# تغيير كلمة المرور
# المدير فقط
# =========================================================

@login_required(login_url="login")
def change_password(request):

    if request.user.role != "admin":
        return redirect("dashboard")

    if request.method == "POST":

        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # التحقق من كلمة المرور الحالية
        if not request.user.check_password(old_password):

            messages.error(
                request,
                "كلمة المرور الحالية غير صحيحة."
            )

            return redirect("change_password")

        # التحقق من تطابق كلمتي المرور
        if new_password != confirm_password:

            messages.error(
                request,
                "كلمتا المرور الجديدتان غير متطابقتين."
            )

            return redirect("change_password")

        # التحقق من طول كلمة المرور
        if len(new_password) < 8:

            messages.error(
                request,
                "يجب أن تتكون كلمة المرور من 8 أحرف أو أرقام على الأقل."
            )

            return redirect("change_password")

        # تغيير كلمة المرور
        request.user.set_password(new_password)
        request.user.save()

        # إبقاء المدير مسجل الدخول
        update_session_auth_hash(
            request,
            request.user
        )

        messages.success(
            request,
            "تم تغيير كلمة المرور بنجاح."
        )

        return redirect("settings")

    return render(
        request,
        "dashboard/change_password.html"
    )


# =========================================================
# من نحن
# =========================================================

def about(request):

    return render(
        request,
        "dashboard/about.html"
    )


# =========================================================
# اتصل بنا
# =========================================================

def contact(request):

    return render(
        request,
        "dashboard/contact.html"
    )


# =========================================================
# صفحة 404
# =========================================================

def page_not_found(request):

    return render(
        request,
        "404.html"
    )


# =========================================================
# نسيت كلمة المرور
# =========================================================

def forgot_password(request):

    return render(
        request,
        "dashboard/forgot_password.html"
    )


# =========================================================
# تسجيل الخروج
# =========================================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "تم تسجيل الخروج بنجاح."
    )

    return redirect("login")