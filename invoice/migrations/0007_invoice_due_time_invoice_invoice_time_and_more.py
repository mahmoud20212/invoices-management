# Generated by Django 4.2.3 on 2023-09-04 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0006_alter_invoice_address_one_alter_invoice_address_two_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='due_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoice_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='time_of_supply',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
