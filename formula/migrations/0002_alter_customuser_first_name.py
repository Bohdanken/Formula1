# Generated by Django 4.2.11 on 2024-03-21 06:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
    ]
