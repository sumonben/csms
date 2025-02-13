# Generated by Django 5.1.4 on 2025-01-19 05:33

import django.db.models.deletion
import smart_selects.db_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_alter_district_division'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='division',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.division'),
        ),
    ]
