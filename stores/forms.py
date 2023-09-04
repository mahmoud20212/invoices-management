from django import forms
from .models import Store


class StoreForm(forms.ModelForm):
    slug = forms.SlugField(required=False)
    tax_number = forms.IntegerField(required=True, min_value=0)
    commercial_record = forms.IntegerField(required=True, min_value=0)
    class Meta:
        model = Store
        fields = [
            'logo',
            'name',
            'tax_number',
            'commercial_record',
            'address',
            'slug',
        ]

    def __init__(self, *args, **kwargs):
        super(StoreForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'