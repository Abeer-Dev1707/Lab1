from .models import Notification
from accounts.models import User


# =========================================================
# إنشاء إشعار لمستخدم محدد
# =========================================================

def create_notification(
    user,
    title,
    message,
    notification_type="system"
):

    if not user:
        return None

    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type
    )


# =========================================================
# إشعار جميع المديرين
# =========================================================

def notify_admins(
    title,
    message,
    notification_type="system"
):

    admins = User.objects.filter(
        role="admin",
        is_active=True
    )

    notifications = []

    for admin in admins:

        notifications.append(
            Notification.objects.create(
                user=admin,
                title=title,
                message=message,
                notification_type=notification_type
            )
        )

    return notifications


# =========================================================
# إشعار جميع الصيادلة
# =========================================================

def notify_pharmacists(
    title,
    message,
    notification_type="system"
):

    pharmacists = User.objects.filter(
        role="pharmacist",
        is_active=True
    )

    notifications = []

    for pharmacist in pharmacists:

        notifications.append(
            Notification.objects.create(
                user=pharmacist,
                title=title,
                message=message,
                notification_type=notification_type
            )
        )

    return notifications


# =========================================================
# إشعار المديرين والصيادلة
# =========================================================

def notify_admins_and_pharmacists(
    title,
    message,
    notification_type="system"
):

    users = User.objects.filter(
        role__in=["admin", "pharmacist"],
        is_active=True
    )

    notifications = []

    for user in users:

        notifications.append(
            Notification.objects.create(
                user=user,
                title=title,
                message=message,
                notification_type=notification_type
            )
        )

    return notifications


# =========================================================
# إشعار مستخدم معين
# =========================================================

def notify_user(
    user,
    title,
    message,
    notification_type="system"
):

    return create_notification(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type
    )