# Generated by Django 4.2.3 on 2023-08-04 12:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('invoice_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('status', models.CharField(choices=[('P', 'Paid'), ('U', 'Unpaid')], default='U', max_length=30)),
                ('name', models.CharField(max_length=255)),
                ('address_one', models.CharField(max_length=255)),
                ('address_two', models.CharField(max_length=255)),
                ('mobile_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('city', models.CharField(max_length=255)),
                ('due_date', models.DateField()),
                ('invoice_date', models.DateField()),
                ('date_of_supply', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='stores.store')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='invoice.invoice')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
