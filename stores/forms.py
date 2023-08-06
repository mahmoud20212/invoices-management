from django import forms
from .models import Store


class StoreForm(forms.ModelForm):
    slug = forms.SlugField(required=False)
    class Meta:
        model = Store
        fields = [
            'logo',
            'name',
            'tax_number',
            'address',
            'slug',
        ]

    def __init__(self, *args, **kwargs):
        super(StoreForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'