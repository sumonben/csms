# Generated by Django 5.1.4 on 2025-05-18 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_alter_paymenttype_options_paymentpurpose_subtitle_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='tran_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
