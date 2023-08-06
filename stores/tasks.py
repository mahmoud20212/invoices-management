import base64
from zipfile import ZipFile
from io import BytesIO
from celery import shared_task
from celery_progress.backend import ProgressRecorder

from invoice.models import Invoice
from invoice.helper import generate_invoice_pdf

@shared_task(bind=True)
def create_zip_invoices(self, options: dict):
    progress_recorder = ProgressRecorder(self)
    invoices = Invoice.objects.filter(store=options['pk'])
    count = invoices.count()
    absolute_uri = options['absolute_uri']
    zip_buffer = BytesIO()

    del options['absolute_uri']
    del options['pk']
    
    with ZipFile(zip_buffer, 'w') as zip_file:
        for index, invoice in enumerate(invoices, 0):
            pdf_content = generate_invoice_pdf(absolute_uri, invoice, **options)
            filename = f'invoice_{invoice.pk}.pdf'
            zip_file.writestr(filename, pdf_content)
            progress_recorder.set_progress(index + 1, count)

    # Convert the zip_buffer to a Base64 encoded string
    encoded_zip = base64.b64encode(zip_buffer.getvalue()).decode('utf-8')

    return encoded_zip