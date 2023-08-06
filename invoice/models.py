import decimal

from django.db import models
from django.core.validators import MinValueValidator

from stores.models import Store


class Invoice(models.Model):
    INVOICE_STATUS = (
        ('P', 'Paid'),
        ('U', 'Unpaid'),
    )
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='invoices')
    tax_number = models.IntegerField(validators=[MinValueValidator(0)])
    invoice_number  = models.IntegerField(validators=[MinValueValidator(0)])
    status  = models.CharField(max_length=30, choices=INVOICE_STATUS, default='U')
    name = models.CharField(max_length=255)
    address_one = models.CharField(max_length=255)
    address_two = models.CharField(max_length=255)
    mobile_number = models.IntegerField(validators=[MinValueValidator(0)])
    city = models.CharField(max_length=255)
    due_date  = models.DateField()
    invoice_date  = models.DateField()
    date_of_supply  = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return self.name
    
    @property
    def total(self):
        total = 0
        for i in self.products.all():
            total += i.total
        return total
    
    @property
    def tax(self):
        # Calculate tax using decimal.Decimal with 2 decimal places
        tax_amount = self.total * decimal.Decimal('0.15')
        tax_amount = tax_amount.quantize(decimal.Decimal('0.00'), rounding=decimal.ROUND_DOWN)
        return tax_amount
    
    @property
    def all_total(self):
        return decimal.Decimal(self.total) + self.tax

class Product(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return self.name
    
    @property
    def total(self):
        return self.quantity * self.price
