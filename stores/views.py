from slugify import slugify

from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.core.exceptions import ValidationError

from invoice.models import Invoice
from .models import Store
from .forms import StoreForm
from .functions import handle_excel_file
from .tasks import create_zip_invoices

def index(request):
    stores = Store.objects.all()
    paginator = Paginator(stores, 50)
    page = request.GET.get('page')
    try:
        stores = paginator.page(page)
    except PageNotAnInteger:
        stores = paginator.page(1)
    except EmptyPage:
        stores = paginator.page(paginator.num_pages)

    return render(request, 'stores/index.html', {'stores': stores})

def create(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            # check if this store exist or not
            slug = slugify(form.cleaned_data['name'], to_lower=True)
            store = Store.objects.filter(slug=slug)
            if not store.exists():
                new_store = form.save(commit=False)
                new_store.slug = slug
                new_store.save()
            else:
                messages.error(request, 'هذا المتجر موجود بالفعل.')
                return render(request, 'stores/create.html', {'form': form})

            messages.success(request, 'تمت إضافة المتجر بنجاح.')
            return redirect('stores:index')
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    else:
        form = StoreForm()
    return render(request, 'stores/create.html', {'form': form})

def create_task(request, store_id):
    options = {
        'color_text_section_1': request.POST.get('color_text_section_1'),
        'color_background_section_1': request.POST.get('color_background_section_1'),
        'color_text_section_2': request.POST.get('color_text_section_2'),
        'color_background_section_2': request.POST.get('color_background_section_2'),
        'color_text_top_bar': request.POST.get('color_text_top_bar'),
        'color_background_top_bar': request.POST.get('color_background_top_bar'),
        'color_text_bottom_bar': request.POST.get('color_text_bottom_bar'),
        'color_background_bottom_bar': request.POST.get('color_background_bottom_bar'),
        'absolute_uri': request.build_absolute_uri(),
        'model_pdf': request.POST.get('model_pdf'),
        'pk': store_id,
    }

    task = create_zip_invoices.delay(options)

    return task

def edit(request, slug):
    store = get_object_or_404(Store, slug=slug)
    form = StoreForm(instance=store)
    store_id = store.id

    # invoices with pagination
    invoices_for_store = store.invoices.all()
    invoices_count = invoices_for_store.count()
    paginator = Paginator(invoices_for_store, 50)
    page = request.GET.get('page')
    try:
        invoices_for_store = paginator.page(page)
    except PageNotAnInteger:
        invoices_for_store = paginator.page(1)
    except EmptyPage:
        invoices_for_store = paginator.page(paginator.num_pages)
    
    if request.method == 'POST':
        # check and create zip file
        if request.POST.get('zip'):
            task = create_task(request, store_id)
            messages.success(request, 'جاري اعداد الملف الرجاء الانتظار حتى الانتهاء من اعداد الملف.')
            return render(
                request,
                'stores/edit.html',
                {
                    'task_id': task.task_id,
                    'form': form,
                    'invoices': invoices_for_store,
                    'invoices_count': invoices_count,
                    'store_id': store_id,
                }
            )
        
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            # check if this store exist or not
            slug = slugify(form.cleaned_data['name'], to_lower=True)
            filter_store = Store.objects.filter(slug=slug).exclude(id=store_id)
            if not filter_store.exists():
                new_store = form.save(commit=False)
                new_store.slug = slug
                new_store.save()
            else:
                messages.error(request, 'هذا المتجر موجود بالفعل.')
                return render(
                    request,
                    'stores/edit.html',
                    {
                        'form': form,
                        'invoices': invoices_for_store,
                        'invoices_count': invoices_count,
                        'store_id': store_id,
                    }
                )
            
            messages.success(request, 'تم تعديل المتجر بنجاح.')
            return redirect(reverse('stores:edit', args=[new_store.slug]))
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    
    return render(
        request,
        'stores/edit.html',
        {
            'form': form,
            'invoices': invoices_for_store,
            'invoices_count': invoices_count,
            'store_id': store_id,
        }
    )

@require_POST
def delete(request, pk):
    store = get_object_or_404(Store, id=pk)
    store.delete()
    messages.success(request, 'تم حذف المتجر بنجاح.')
    return redirect('stores:index')

@require_POST
def delete_all_invoices(request, pk):
    store = get_object_or_404(Store, id=pk)
    Invoice.objects.filter(store=store).delete()
    messages.success(request, 'تم حذف فواتير المتجر بنجاح.')
    return redirect(reverse('stores:edit', args=[store.slug]))

@require_POST
def upload_for_store(request, pk):
    store = get_object_or_404(Store, id=pk)
    try:
        handle_excel_file(request, store)
        messages.success(request, 'تم اضافة الفواتير بنجاح.')
    except ValidationError as e:
        messages.error(request, str(e.message))
    
    return redirect(reverse('stores:edit', args=[store.slug]))