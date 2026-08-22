from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from django.utils import timezone

from medicines.models import Medicine
from customers.models import Customer
from suppliers.models import Supplier
from purchases.models import PurchaseOrder
from sales.models import Sale, SaleItem


# =========================================================
# صفحة التقارير
# المدير + الصيدلي
# =========================================================

@login_required(login_url="login")
def reports_home(request):

    # -----------------------------------------------------
    # الصلاحيات
    # -----------------------------------------------------

    if request.user.role not in ["admin", "pharmacist"]:

        return render(
            request,
            "dashboard/dashboard.html",
            {
                "error_message":
                    "غير مسموح لك بالوصول إلى التقارير."
            }
        )

    # -----------------------------------------------------
    # التاريخ الحالي
    # -----------------------------------------------------

    today = timezone.localdate()

    # =====================================================
    # المبيعات
    # =====================================================

    completed_sales = Sale.objects.filter(
        status="completed"
    )

    cancelled_sales = Sale.objects.filter(
        status="cancelled"
    )

    sales_count = completed_sales.count()

    cancelled_sales_count = cancelled_sales.count()

    total_sales = (
        completed_sales.aggregate(
            total=Sum("total_amount")
        )["total"] or 0
    )

    # -----------------------------------------------------
    # مبيعات اليوم
    # -----------------------------------------------------

    today_sales = completed_sales.filter(
        created_at__date=today
    )

    today_sales_count = today_sales.count()

    today_sales_total = (
        today_sales.aggregate(
            total=Sum("total_amount")
        )["total"] or 0
    )

    # =====================================================
    # الرسم البياني للمبيعات
    # آخر 6 أشهر
    # =====================================================

    current_month = today.replace(
        day=1
    )

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
    # المبيعات الشهرية
    # -----------------------------------------------------

    monthly_sales_queryset = (
        completed_sales
        .filter(
            created_at__date__gte=months[0],
            created_at__date__lte=today
        )
        .annotate(
            month=TruncMonth(
                "created_at"
            )
        )
        .values(
            "month"
        )
        .annotate(
            total=Sum(
                "total_amount"
            )
        )
        .order_by(
            "month"
        )
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

    # -----------------------------------------------------
    # تجهيز بيانات الرسم البياني
    # -----------------------------------------------------

    sales_chart = []

    for month in months:

        sales_chart.append(
            {
                "label":
                    month_names[
                        month.month
                    ],

                "value":
                    monthly_sales.get(
                        month,
                        0
                    ),
            }
        )

    # -----------------------------------------------------
    # أعلى قيمة في الرسم البياني
    # -----------------------------------------------------

    chart_max_value = max(
        (
            item["value"]
            for item in sales_chart
        ),
        default=0
    )

    # منع القسمة على صفر
    # عندما لا توجد أي مبيعات

    if chart_max_value <= 0:

        chart_max_value = 1

    # =====================================================
    # المخزون
    # =====================================================

    medicines = Medicine.objects.all()

    medicines_count = medicines.count()

    total_stock_quantity = (
        medicines.aggregate(
            total=Sum("quantity")
        )["total"] or 0
    )

    # -----------------------------------------------------
    # الأدوية منخفضة المخزون
    # -----------------------------------------------------

    low_stock_queryset = medicines.filter(
        quantity__gt=0,
        quantity__lte=F(
            "minimum_stock"
        )
    )

    low_stock_count = (
        low_stock_queryset.count()
    )

    low_stock_medicines = (
        low_stock_queryset
        .order_by(
            "quantity",
            "name"
        )[:10]
    )

    # -----------------------------------------------------
    # الأدوية النافدة
    # -----------------------------------------------------

    out_of_stock_count = (
        medicines
        .filter(
            quantity=0
        )
        .count()
    )

    # =====================================================
    # العملاء والموردون
    # =====================================================

    customers_count = (
        Customer.objects.count()
    )

    suppliers_count = (
        Supplier.objects.count()
    )

    # =====================================================
    # طلبات التوريد
    # =====================================================

    purchase_orders_count = (
        PurchaseOrder.objects.count()
    )

    pending_purchase_orders = (
        PurchaseOrder.objects
        .filter(
            status="pending"
        )
        .count()
    )

    approved_purchase_orders = (
        PurchaseOrder.objects
        .filter(
            status="approved"
        )
        .count()
    )

    completed_purchase_orders = (
        PurchaseOrder.objects
        .filter(
            status="completed"
        )
        .count()
    )

    rejected_purchase_orders = (
        PurchaseOrder.objects
        .filter(
            status="rejected"
        )
        .count()
    )

    # =====================================================
    # آخر المبيعات
    # =====================================================

    latest_sales = (
        completed_sales
        .select_related(
            "customer",
            "cashier"
        )
        .prefetch_related(
            "items"
        )
        .order_by(
            "-created_at"
        )[:10]
    )

    # =====================================================
    # أكثر المنتجات مبيعًا
    # =====================================================

    best_selling_products = (
        SaleItem.objects
        .filter(
            sale__status="completed"
        )
        .values(
            "medicine__name"
        )
        .annotate(
            total_quantity=Sum(
                "quantity"
            ),
            total_amount=Sum(
                "subtotal"
            )
        )
        .order_by(
            "-total_quantity"
        )[:10]
    )

    # =====================================================
    # بيانات الصفحة
    # =====================================================

    context = {

        # -------------------------------------------------
        # الإحصائيات الأساسية
        # -------------------------------------------------

        "medicines_count":
            medicines_count,

        "customers_count":
            customers_count,

        "suppliers_count":
            suppliers_count,

        "purchase_orders_count":
            purchase_orders_count,

        # -------------------------------------------------
        # المبيعات
        # -------------------------------------------------

        "sales_count":
            sales_count,

        "cancelled_sales_count":
            cancelled_sales_count,

        "total_sales":
            total_sales,

        "today_sales_count":
            today_sales_count,

        "today_sales_total":
            today_sales_total,

        # -------------------------------------------------
        # المخزون
        # -------------------------------------------------

        "total_stock_quantity":
            total_stock_quantity,

        "low_stock_count":
            low_stock_count,

        "low_stock_medicines":
            low_stock_medicines,

        "out_of_stock_count":
            out_of_stock_count,

        # -------------------------------------------------
        # طلبات التوريد
        # -------------------------------------------------

        "pending_purchase_orders":
            pending_purchase_orders,

        "approved_purchase_orders":
            approved_purchase_orders,

        "completed_purchase_orders":
            completed_purchase_orders,

        "rejected_purchase_orders":
            rejected_purchase_orders,

        # -------------------------------------------------
        # آخر المبيعات
        # -------------------------------------------------

        "latest_sales":
            latest_sales,

        # -------------------------------------------------
        # أكثر المنتجات مبيعًا
        # -------------------------------------------------

        "best_selling_products":
            best_selling_products,

        # -------------------------------------------------
        # الرسم البياني
        # -------------------------------------------------

        "sales_chart":
            sales_chart,

        "chart_max_value":
            chart_max_value,
    }

    return render(
        request,
        "reports/reports.html",
        context
    )