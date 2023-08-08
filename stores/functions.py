import pandas as pd
import random
import math
from datetime import datetime

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
        invoices = []
        for index, row in df.iterrows():
            if pd.isna(row['INVOICE NUMBER']) and pd.isna(row['MOBILE NUMBER']) and pd.isna(row['DATE']) and pd.isna(row['STATUS']):
                continue
            
            status = 'P' if row['STATUS'] == 'مدفوعة' else 'U'
            invoice_number = int(row['INVOICE NUMBER']) if not math.isnan(row['INVOICE NUMBER']) else None
            mobile_number = int(row['MOBILE NUMBER']) if not math.isnan(row['MOBILE NUMBER']) else None
            date_string = str(row['DATE'])
            input_datetime = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
            output_date_string = input_datetime.strftime("%Y-%m-%d")
            invoices.append(
                Invoice(
                    store = store,
                    tax_number = random.randint(0, 9999999999),
                    invoice_number = invoice_number,
                    status = status,
                    name = row['الاسم'],
                    address_one = fake.address(),
                    address_two = fake.address(),
                    mobile_number = mobile_number,
                    city = fake.city(),
                    due_date = output_date_string,
                    invoice_date = output_date_string,
                    date_of_supply = output_date_string,
                )
            )
        if len(invoices):
            Invoice.objects.bulk_create(invoices)
        else:
            raise ValidationError('لا يوجد بيانات في هذا الملف.')
    else:
        raise ValidationError('الرجاء ارفاق ملف لاستيراده.')