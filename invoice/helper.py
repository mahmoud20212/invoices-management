import os
import weasyprint
from django.template.loader import render_to_string
from io import BytesIO
from django.conf import settings


def generate_invoice_pdf(absolute_uri, invoice, *args, **kwargs):
    html = render_to_string(
        'invoice/pdf/pdf_one.html',
        {
            'invoice': invoice,
            'color_text_section_1': kwargs.get('color_text_section_1'),
            'color_background_section_1': kwargs.get('color_background_section_1'),
            'color_text_section_2': kwargs.get('color_text_section_2'),
            'color_background_section_2': kwargs.get('color_background_section_2'),
            'color_text_top_bar': kwargs.get('color_text_top_bar'),
            'color_background_top_bar': kwargs.get('color_background_top_bar'),
            'color_text_bottom_bar': kwargs.get('color_text_bottom_bar'),
            'color_background_bottom_bar': kwargs.get('color_background_bottom_bar'),
        }
    )
    out = BytesIO()
    stylesheets = [
        weasyprint.CSS('https://invoices-management-demo.s3.eu-west-2.amazonaws.com/static/css/pdf.css')
    ]
    weasyprint.HTML(string=html, base_url=absolute_uri).write_pdf(out, stylesheets=stylesheets)
    return out.getvalue()

# old
# @require_POST
# def export(request, pk):
#     # uploaded_file = request.FILES.get('company_logo')
#     # pressure = request.POST.get('pressure')
#     # company_name = request.POST.get('company_name')
#     # company_tax_number = request.POST.get('company_tax_number')

#     # Assuming you have the necessary imports and other setup here.
#     invoice = get_object_or_404(Invoice, id=pk)

#     # if uploaded_file and company_name and company_tax_number:
#     #     try:
#     #         image = Image.open(uploaded_file)
#     #         if pressure:
#     #             if image.height > 300 or image.width > 300:
#     #                 image.thumbnail((300, 300))
#     #         data = BytesIO()
#     #         image.save(data, image.format)
#     #         encoded_img_data = base64.b64encode(data.getvalue()).decode('utf-8')
#     #     except Exception as e:
#     #         messages.error(request, 'حدث خطأ ما الرجاء المحاولة فيما بعد!!')
#     #         return redirect(request.META.get('HTTP_REFERER'))
#     # else:
#     #     encoded_img_data = None
#     #     messages.error(request, 'الرجاء التأكد من اضافة شعار الشركة واسم الشركة والرقم الضريبي!!')
#     #     return redirect(request.META.get('HTTP_REFERER'))
    
#     html = render_to_string(
#         'invoice/pdf/pdf_one.html',
#         {
#             'invoice': invoice,
#             # 'company_name': company_name,
#             # 'company_tax_number': company_tax_number,
#             # 'logo': encoded_img_data # data:image/jpeg;base64,{{ logo }}
#         }
#     )
#     out = BytesIO()
#     stylesheets = [
#         weasyprint.CSS(os.path.join('static/css/pdf.css'))
#     ]

#     weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(out, stylesheets=stylesheets)

#     # Create an HTTP response with the PDF file as content.
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="invoice_{pk}.pdf"'
#     response.write(out.getvalue())

#     return response