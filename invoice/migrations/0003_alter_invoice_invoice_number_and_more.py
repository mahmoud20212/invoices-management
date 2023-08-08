# Generated by Django 4.2.3 on 2023-08-08 14:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_alter_product_price_alter_product_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.BigIntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='tax_number',
            field=models.BigIntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
