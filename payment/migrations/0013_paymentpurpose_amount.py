# Generated by Django 5.1.4 on 2025-06-18 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0012_merge_20250618_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentpurpose',
            name='amount',
            field=models.IntegerField(default=10),
        ),
    ]
