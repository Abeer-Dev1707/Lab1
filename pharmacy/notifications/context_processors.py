from .models import Notification


def notifications_context(request):

    if not request.user.is_authenticated:

        return {
            "notifications": [],
            "unread_notifications_count": 0,
        }

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )[:10]

    unread_notifications_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return {
        "notifications": notifications,
        "unread_notifications_count": unread_notifications_count,
    }