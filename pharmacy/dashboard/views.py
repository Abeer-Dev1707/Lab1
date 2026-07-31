from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from categories.models import Category


def login_view(request):

    # إذا كان المستخدم مسجلاً دخوله بالفعل
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                f"مرحباً {user.username}، تم تسجيل الدخول بنجاح."
            )

            return redirect("dashboard")

        else:

            messages.error(
                request,
                "اسم المستخدم أو كلمة المرور غير صحيحة."
            )

    return render(request, "dashboard/login.html")

from categories.models import Category

@login_required(login_url="login")
def home(request):

    categories = Category.objects.all()

    context = {
        "categories": categories,
    }

    return render(
    request,
    "dashboard/dashboard.html",
    context
)


def about(request):
    return render(request, "dashboard/about.html")


def contact(request):
    return render(request, "dashboard/contact.html")


def page_not_found(request):
    return render(request, "404.html")


def forgot_password(request):
    return render(request, "dashboard/forgot_password.html")


def logout_view(request):

    logout(request)

    messages.success(
        request,
        "تم تسجيل الخروج بنجاح."
    )

    return redirect("login")