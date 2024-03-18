# Generated by Django 2.2.28 on 2024-03-15 23:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formula', '0011_auto_20240315_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='student_id',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator('^[0-9]{7}$', 'Only 7-digit integers are allowed.')]),
        ),
    ]
