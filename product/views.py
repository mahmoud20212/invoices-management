from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.http import require_POST
from django.contrib import messages

from invoice.models import Product
from .forms import ProductForm

def index(request):
    products = Product.objects.all()
    
    paginator = Paginator(products, 50)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    return render(request, 'product/index.html', {'products': products})

def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تمت إضافة المنتج بنجاح.')
            return redirect('product:index')
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    else:
        form = ProductForm()
    return render(request, 'product/form.html', {'form': form})

def edit(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل المنتج بنجاح.')
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/form.html', {'form': form, 'product_id': product.id, 'edit': True})

@require_POST
def delete(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=pk)
        product.delete()
        messages.success(request, 'تم حذف المنتج بنجاح.')
    return redirect('product:index')
