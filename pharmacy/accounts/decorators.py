from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages


# =========================================================
# صلاحية المدير
# =========================================================

def admin_required(view_func):

    @login_required(login_url="login")
    def wrapper(request, *args, **kwargs):

        if request.user.role != "admin":

            messages.error(
                request,
                "🚫 غير مسموح بالدخول! ليس لديك صلاحية للوصول إلى هذه الصفحة."
            )

            return redirect("dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper


# =========================================================
# صلاحية المدير + الصيدلي
# =========================================================

def pharmacist_required(view_func):

    @login_required(login_url="login")
    def wrapper(request, *args, **kwargs):

        allowed_roles = [
            "admin",
            "pharmacist",
        ]

        if request.user.role not in allowed_roles:

            messages.error(
                request,
                "🚫 غير مسموح بالدخول! هذه الصفحة مخصصة للمدير والصيدلي."
            )

            return redirect("dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper


# =========================================================
# صلاحية المدير + الصيدلي + العميل
# =========================================================

def customer_required(view_func):

    @login_required(login_url="login")
    def wrapper(request, *args, **kwargs):

        allowed_roles = [
            "admin",
            "pharmacist",
            "customer",
        ]

        if request.user.role not in allowed_roles:

            messages.error(
                request,
                "🚫 غير مسموح بالدخول! ليس لديك صلاحية للوصول إلى هذه الصفحة."
            )

            return redirect("dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper


# =========================================================
# صلاحية المدير + الصيدلي + المورد
# =========================================================

def supplier_required(view_func):

    @login_required(login_url="login")
    def wrapper(request, *args, **kwargs):

        allowed_roles = [
            "admin",
            "pharmacist",
            "supplier",
        ]

        if request.user.role not in allowed_roles:

            messages.error(
                request,
                "🚫 غير مسموح بالدخول! ليس لديك صلاحية للوصول إلى هذه الصفحة."
            )

            return redirect("dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper