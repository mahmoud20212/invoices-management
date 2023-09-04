from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    invoice_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_of_supply = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    due_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    invoice_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    time_of_supply = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))

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