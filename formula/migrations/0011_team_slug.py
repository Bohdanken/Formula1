# Generated by Django 4.2.11 on 2024-03-18 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formula', '0010_auto_20240314_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='slug',
            field=models.SlugField(default='-'),
            preserve_default=False,
        ),
    ]
