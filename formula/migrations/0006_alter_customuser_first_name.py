# Generated by Django 4.2.11 on 2024-03-21 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formula', '0005_auto_20240321_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
