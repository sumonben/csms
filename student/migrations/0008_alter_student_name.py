# Generated by Django 5.1.4 on 2025-06-05 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_alter_choice_options_alter_session_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Name In English:'),
        ),
    ]
