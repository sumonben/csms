# Generated by Django 5.1.4 on 2025-02-07 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0013_testmarks_total1_testmarks_total2'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='cgpa_without_4th',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='cgpa',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
