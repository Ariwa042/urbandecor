# product/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, Category
from .forms import ProductForm
from django.utils.text import slugify

def product_list(request):
    products = Product.objects.filter(is_available=True)
    category = request.GET.get('category')
    search_query = request.GET.get('q')

    if category:
        products = products.filter(category__slug=category)
    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'product/product_list.html', {
        'products': products,
        'categories': Category.objects.all(),
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=slugify(pk))
    return render(request, 'product/product_detail.html', {'product': product})


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product:product_list')
    else:
        form = ProductForm()
    return render(request, 'product/product_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/product_form.html', {'form': form, 'product': product})


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product:product_list')
    return render(request, 'product/product_confirm_delete.html', {'product': product})
