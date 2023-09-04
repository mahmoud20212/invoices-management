from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'store',
            'invoice_number',
            'status',
            'name',
            'address_one',
            'address_two',
            'mobile_number',
            'city',
            'due_date',
            'invoice_date',
            'date_of_supply',
            'due_time',
            'invoice_time',
            'time_of_supply',
            'show_invoice_time',
            'show_due_time',
            'show_time_of_supply',
        ]

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'