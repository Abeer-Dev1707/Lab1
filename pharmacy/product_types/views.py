from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import ProductType
from .forms import ProductTypeForm


def product_type_list(request):

    search = request.GET.get("search", "")

    product_types = ProductType.objects.all()

    if search:

        product_types = product_types.filter(

            Q(name__icontains=search) |
            Q(description__icontains=search)

        )

    paginator = Paginator(product_types, 10)

    page_number = request.GET.get("page")

    product_types = paginator.get_page(page_number)

    return render(request, "product_types/product_type_list.html", {

        "product_types": product_types,

        "search": search,

    })


def product_type_create(request):

    if request.method == "POST":

        form = ProductTypeForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "تمت إضافة نوع المنتج بنجاح.")

            return redirect("product_type_list")

    else:

        form = ProductTypeForm()

    return render(request, "product_types/product_type_form.html", {

        "form": form,

        "page_title": "إضافة نوع منتج",

    })


def product_type_update(request, pk):

    product_type = get_object_or_404(ProductType, pk=pk)

    if request.method == "POST":

        form = ProductTypeForm(request.POST, instance=product_type)

        if form.is_valid():

            form.save()

            messages.success(request, "تم تعديل نوع المنتج بنجاح.")

            return redirect("product_type_list")

    else:

        form = ProductTypeForm(instance=product_type)

    return render(request, "product_types/product_type_form.html", {

        "form": form,

        "page_title": "تعديل نوع المنتج",

    })


def product_type_delete(request, pk):

    product_type = get_object_or_404(ProductType, pk=pk)

    if request.method == "POST":

        product_type.delete()

        messages.success(request, "تم حذف نوع المنتج بنجاح.")

        return redirect("product_type_list")

    return render(request, "product_types/product_type_delete.html", {

        "product_type": product_type

    })