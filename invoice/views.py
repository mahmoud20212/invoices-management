import pandas as pd
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse

from .models import Invoice
from .forms import InvoiceForm
from .helper import generate_invoice_pdf


def index(request):
    invoices = Invoice.objects.all()
    
    paginator = Paginator(invoices, 50)
    page = request.GET.get('page')
    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        invoices = paginator.page(1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)
    
    return render(request, 'invoice/index.html', {'invoices': invoices, 'page': page})

def create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تمت إضافة الفاتورة بنجاح.')
            return redirect('index')
        else:
            return render(request, 'invoice/create.html', {'form': form})
    else:
        form = InvoiceForm()
    return render(request, 'invoice/create.html', {'form': form})

def edit(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل الفاتورة بنجاح.')
            return redirect(reverse('edit', args=[pk]))
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    else:
        form = InvoiceForm(instance=invoice)

    return render(request, 'invoice/edit.html', {'form': form, 'invoice': invoice})

@require_POST
def delete(request, pk):
    if request.method == 'POST':
        invoice = get_object_or_404(Invoice, id=pk)
        invoice.delete()
        messages.success(request, 'تم حذف الفاتورة بنجاح.')
    return redirect('index')

@require_POST
def upload(request):
    excel_file = request.FILES.get('excel_file')
    format_specifier = "%Y-%m-%d %H:%M:%S"
    
    if excel_file:
        df = pd.read_excel(excel_file)

        for index, row in df.iterrows():
            if pd.isna(row['INVOICE NUMBER']):
                continue
            
            status = 'P' if row['STATUS'] == 'مدفوعة' else 'U'
            invoice = Invoice(
                invoice_number = int(row['INVOICE NUMBER']),
                name = row['الاسم'],
                mobile_number = int(row['MOBILE NUMBER']),
                invoice_date = datetime.strptime(row['DATE'], format_specifier),
                status = status,
                value_added = row['القيمة'],
            )
            invoice.save()

    return redirect('index')

@require_POST
def export(request, pk):
    options = {
        'color_text_section_1': request.POST.get('color_text_section_1'),
        'color_background_section_1': request.POST.get('color_background_section_1'),
        'color_text_section_2': request.POST.get('color_text_section_2'),
        'color_background_section_2': request.POST.get('color_background_section_2'),
        'color_text_top_bar': request.POST.get('color_text_top_bar'),
        'color_background_top_bar': request.POST.get('color_background_top_bar'),
        'color_text_bottom_bar': request.POST.get('color_text_bottom_bar'),
        'color_background_bottom_bar': request.POST.get('color_background_bottom_bar'),
        'model_pdf': request.POST.get('model_pdf'),
    }
    
    invoice = get_object_or_404(Invoice, id=pk)

    absolute_uri = request.build_absolute_uri()
    value = generate_invoice_pdf(absolute_uri, invoice, **options)

    # Create an HTTP response with the PDF file as content.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{pk}.pdf"'
    response.write(value)

    return response

# @require_POST
# def zip_invoices(request, pk):
#     invoices = Invoice.objects.filter(store=pk)
#     if not invoices.exists():
#         messages.error(request, 'لا يوجد فواتير لهذا المتجر الرجاء اضافة فواتير لبدا التصدير.')
#         return redirect(request.META.get('HTTP_REFERER'))
    
#     options = {
#         'color_text_section_1': request.POST.get('color_text_section_1'),
#         'color_background_section_1': request.POST.get('color_background_section_1'),
#         'color_text_section_2': request.POST.get('color_text_section_2'),
#         'color_background_section_2': request.POST.get('color_background_section_2'),
#         'color_text_top_bar': request.POST.get('color_text_top_bar'),
#         'color_background_top_bar': request.POST.get('color_background_top_bar'),
#         'color_text_bottom_bar': request.POST.get('color_text_bottom_bar'),
#         'color_background_bottom_bar': request.POST.get('color_background_bottom_bar'),
#         'absolute_uri': request.build_absolute_uri(),
#         'pk': pk,
#     }

#     task = create_zip_invoices.delay(options)
#     # messages.success(request, 'جاري العمل على تصدير كل الفواتير الرجاء تفحص الايميل الخاص بك بعد قليل.')
#     # return redirect(reverse('stores:edit', args=[pk]))
#     return render(request, 'invoice/progress.html', {'task_id': task.task_id})

# def show_invoice(request, pk):
#     invoice = get_object_or_404(Invoice, id=pk)
#     return render(request, 'invoice/pdf/pdf_one.html', {'invoice': invoice})