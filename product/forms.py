from django import forms
from invoice.models import Product, Invoice

class ProductForm(forms.ModelForm):
    invoice = forms.ModelChoiceField(queryset=Invoice.objects.all())
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'