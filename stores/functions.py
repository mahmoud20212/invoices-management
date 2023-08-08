import pandas as pd
from datetime import datetime
import random

from faker import Faker

from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from invoice.models import Invoice

fake = Faker()

def handle_excel_file(request, store):
    excel_file = request.FILES.get('excel_file')
    
    if excel_file:
        # List of allowed file extensions
        allowed_extensions = ['xlsx']
        # Use FileExtensionValidator to check if the file extension is allowed
        file_validator = FileExtensionValidator(allowed_extensions)

        try:
            file_validator(excel_file)
        except ValidationError:
            raise ValidationError('هذا الملف غير صالح.')
        
        df = pd.read_excel(excel_file)
        format_specifier = "%Y-%m-%d %H:%M:%S"
        invoices = []
        for index, row in df.iterrows():
            if pd.isna(row['INVOICE NUMBER']):
                continue
            
            status = 'P' if row['STATUS'] == 'مدفوعة' else 'U'
            invoice = Invoice(
                store = store,
                tax_number = random.randint(0, 9999999999),
                invoice_number = int(row['INVOICE NUMBER']),
                status = status,
                name = row['الاسم'],
                address_one = fake.address(),
                address_two = fake.address(),
                mobile_number = int(row['MOBILE NUMBER']),
                city = fake.city(),
                due_date = datetime.strptime(row['DATE'], format_specifier),
                invoice_date = datetime.strptime(row['DATE'], format_specifier),
                date_of_supply = datetime.strptime(row['DATE'], format_specifier),
            )
            invoice.save()
        # if len(invoices):
        #     Invoice.objects.bulk_create(invoices)
        # else:
        #     raise ValidationError('لا يوجد بيانات في هذا الملف.')
    else:
        raise ValidationError('الرجاء ارفاق ملف لاستيراده.')