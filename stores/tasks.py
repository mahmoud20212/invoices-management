import base64
import traceback
from zipfile import ZipFile
from io import BytesIO
from celery import shared_task
from celery_progress.backend import ProgressRecorder

from invoice.models import Invoice
from invoice.helper import generate_invoice_pdf

@shared_task(bind=True)
def create_zip_invoices(self, options: dict):
    try:
        progress_recorder = ProgressRecorder(self)
        invoices = Invoice.objects.filter(store=options['pk'])
        count = invoices.count()
        absolute_uri = options['absolute_uri']
        zip_buffer = BytesIO()

        del options['absolute_uri']
        del options['pk']

        chunk_size = 20  # Experiment with different chunk sizes
        for start_index in range(0, count, chunk_size):
            end_index = min(start_index + chunk_size, count)
            chunk_invoices = invoices[start_index:end_index]

            with ZipFile(zip_buffer, 'a') as zip_file:
                for index, invoice in enumerate(chunk_invoices, start=start_index):
                    pdf_content = generate_invoice_pdf(absolute_uri, invoice, **options)
                    filename = f'invoice_{invoice.pk}.pdf'
                    zip_file.writestr(filename, pdf_content)
                    progress_recorder.set_progress(index + 1, count)

        # Convert the zip_buffer to a Base64 encoded string
        encoded_zip = base64.b64encode(zip_buffer.getvalue()).decode('utf-8')
        
        return encoded_zip
    except Exception as e:
        traceback_str = traceback.format_exc()
        # Log the traceback_str or use your preferred logging mechanism
        print(traceback_str)
        raise e


# @shared_task(bind=True)
# def create_zip_invoices(self, options: dict):
#     progress_recorder = ProgressRecorder(self)
#     invoices = Invoice.objects.filter(store=options['pk'])
#     count = invoices.count()
#     absolute_uri = options['absolute_uri']
#     zip_buffer = BytesIO()

#     del options['absolute_uri']
#     del options['pk']
    
#     with ZipFile(zip_buffer, 'w') as zip_file:
#         for index, invoice in enumerate(invoices, 0):
#             pdf_content = generate_invoice_pdf(absolute_uri, invoice, **options)
#             filename = f'invoice_{invoice.pk}.pdf'
#             zip_file.writestr(filename, pdf_content)
#             progress_recorder.set_progress(index + 1, count)

#     # Convert the zip_buffer to a Base64 encoded string
#     encoded_zip = base64.b64encode(zip_buffer.getvalue()).decode('utf-8')

#     return encoded_zip