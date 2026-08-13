from django.shortcuts import render
from .models import Category
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CategoryForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from django.db.models import Q

from accounts.decorators import pharmacist_required


@pharmacist_required
def category_list(request):

    search = request.GET.get('search', '')

    categories = Category.objects.all()

    if search:
        categories = categories.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    # إنشاء ترقيم الصفحات (5 عناصر في كل صفحة)
    paginator = Paginator(categories, 5)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request, 'categories/category_list.html', {
        'page_obj': page_obj,
        'search': search,
    })


@pharmacist_required
def category_create(request):

    if request.method == 'POST':

        form = CategoryForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "تمت إضافة الفئة بنجاح."
            )

            return redirect('category_list')

    else:

        form = CategoryForm()

    return render(request, 'categories/category_form.html', {
        'form': form,
        'page_title': 'إضافة فئة'
    })


@pharmacist_required
def category_update(request, pk):

    category = get_object_or_404(
        Category,
        pk=pk
    )

    if request.method == 'POST':

        form = CategoryForm(
            request.POST,
            instance=category
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "تم تعديل الفئة بنجاح."
            )

            return redirect('category_list')

    else:

        form = CategoryForm(
            instance=category
        )

    return render(request, 'categories/category_form.html', {
        'form': form,
        'page_title': 'تعديل الفئة'
    })


@pharmacist_required
def category_delete(request, pk):

    category = get_object_or_404(
        Category,
        pk=pk
    )

    if request.method == "POST":

        category.delete()

        messages.success(
            request,
            "تم حذف الفئة بنجاح."
        )

        return redirect("category_list")

    return render(request, "categories/category_delete.html", {
        "category": category
    })