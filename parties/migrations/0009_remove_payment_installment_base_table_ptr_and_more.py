# Generated by Django 5.0 on 2024-01-12 09:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0008_payment_installment_base_table_ptr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment_installment',
            name='base_table_ptr',
        ),
        migrations.AlterField(
            model_name='payment_installment',
            name='paid_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
