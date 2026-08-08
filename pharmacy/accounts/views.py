from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User
from .forms import UserForm
from django.db.models import Q
from django.core.paginator import Paginator


def user_list(request):

    search = request.GET.get("search", "")

    users = User.objects.all()

    if search:

        users = users.filter(

            Q(full_name__icontains=search) |
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)

        )

    paginator = Paginator(users, 10)

    page_number = request.GET.get("page")

    users = paginator.get_page(page_number)

    return render(request, "accounts/user_list.html", {

        "users": users,

        "search": search,

    })


def user_create(request):

    if request.method == "POST":

        form = UserForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "تمت إضافة المستخدم بنجاح.")

            return redirect("user_list")

    else:

        form = UserForm()

    return render(request, "accounts/user_form.html", {

        "form": form,

        "page_title": "إضافة مستخدم",

    })


def user_update(request, pk):

    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":

        form = UserForm(request.POST, instance=user)

        if form.is_valid():

            form.save()

            messages.success(request, "تم تعديل المستخدم بنجاح.")

            return redirect("user_list")

    else:

        form = UserForm(instance=user)

    return render(request, "accounts/user_form.html", {

        "form": form,

        "page_title": "تعديل المستخدم",

    })


def user_delete(request, pk):

    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":

        user.delete()

        messages.success(request, "تم حذف المستخدم بنجاح.")

        return redirect("user_list")

    return render(request, "accounts/user_delete.html", {

        "user": user

    })