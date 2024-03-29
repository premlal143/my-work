# Generated by Django 5.0 on 2024-01-07 08:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labor', '0002_labor_register_otp'),
        ('parties', '0003_task_labor_id_task_remaining_payment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='labor_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labor.labor_register'),
        ),
        migrations.AlterField(
            model_name='task',
            name='remaining_payment',
            field=models.FloatField(blank=True),
        ),
    ]
