from django.contrib import admin
from .models import Invoice, Product

# Register your models here.
admin.site.register(Invoice)
admin.site.register(Product)