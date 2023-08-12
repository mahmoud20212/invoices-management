# import pandas as pd
import openpyxl
from datetime import datetime

# from faker import Faker

from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from invoice.models import Invoice

# fake = Faker()

def read_excel_and_exclude_empty_rows(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    
    data = []
    column_names = None  # To store the header row
    
    for row in sheet.iter_rows(values_only=True):
        if column_names is None:
            column_names = row
        elif all(cell is not None for cell in row):
            data.append(row)
    
    return column_names, data

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

        column_names, result = read_excel_and_exclude_empty_rows(excel_file)

        invoices = []
        for row in result:
            # Create a dictionary that maps column names to cell values
            row_dict = {column_names[i]: value for i, value in enumerate(row)}
            
            # Access cells by column name
            # print("Column NAME", row_dict['الاسم'])
            # print("Column INVOICE NUMBER:", row_dict['INVOICE NUMBER'])
            # print("Column MOBILE NUMBER:", row_dict['MOBILE NUMBER'])
            # print("Column STATUS:", row_dict['STATUS'])
            # print("Column DATE:", row_dict['DATE'])
            
            name = row_dict['الاسم']
            invoice_number = row_dict['INVOICE NUMBER']
            mobile_number = row_dict['MOBILE NUMBER']
            status = 'P' if row_dict['STATUS'] == 'مدفوعة' else 'U'
            
            # convert date for accept format in django
            date_string = str(row_dict['DATE'])
            input_datetime = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
            output_date_string = input_datetime.strftime("%Y-%m-%d")
            
            invoices.append(
                Invoice(
                    store = store,
                    invoice_number = invoice_number,
                    status = status,
                    name = name,
                    mobile_number = mobile_number,
                    invoice_date = output_date_string,
                    address_one = None,
                    address_two = None,
                    city = None,
                    due_date = None,
                    date_of_supply = None,
                )
            )
        if len(invoices):
            Invoice.objects.bulk_create(invoices)
        else:
            raise ValidationError('لا يوجد بيانات في هذا الملف.')
    else:
        raise ValidationError('الرجاء ارفاق ملف لاستيراده.')