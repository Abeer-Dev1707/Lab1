from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Notification


# =========================================================
# جميع الإشعارات
# =========================================================

@login_required(login_url="login")
def notification_list(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )

    unread_notifications_count = notifications.filter(
        is_read=False
    ).count()

    return render(
        request,
        "notifications/notification_list.html",
        {
            "notifications": notifications,
            "unread_notifications_count": unread_notifications_count,
        }
    )


# =========================================================
# تفاصيل الإشعار
# =========================================================

@login_required(login_url="login")
def notification_detail(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )

    # -----------------------------------------
    # تحديد الإشعار كمقروء
    # -----------------------------------------

    if not notification.is_read:

        notification.is_read = True

        notification.save(
            update_fields=["is_read"]
        )

    return render(
        request,
        "notifications/notification_detail.html",
        {
            "notification": notification,
        }
    )


# =========================================================
# تحديد جميع الإشعارات كمقروءة
# =========================================================

@login_required(login_url="login")
def mark_all_read(request):

    if request.method == "POST":

        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(
            is_read=True
        )

    return redirect(
        "notifications"
    )


# =========================================================
# حذف الإشعار
# =========================================================

@login_required(login_url="login")
def notification_delete(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        notification.delete()

    return redirect(
        "notifications"
    )