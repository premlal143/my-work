# Generated by Django 5.0 on 2023-12-30 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='labor_register',
            name='otp',
            field=models.CharField(default='569864', max_length=50),
        ),
    ]
