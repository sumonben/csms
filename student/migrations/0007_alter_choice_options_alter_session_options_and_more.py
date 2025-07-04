# Generated by Django 5.1.4 on 2025-05-18 14:18

import student.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_subject_is_practical_alter_student_image_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choice',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='student',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=student.models.rename_image),
        ),
    ]
