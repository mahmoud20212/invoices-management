# Generated by Django 4.2.3 on 2023-08-12 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_remove_invoice_tax_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='address_one',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='address_two',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date_of_supply',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(null=True),
        ),
    ]