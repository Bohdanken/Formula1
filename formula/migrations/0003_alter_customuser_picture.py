# Generated by Django 4.2.11 on 2024-03-21 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formula', '0002_alter_customuser_first_name_alter_customuser_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='picture',
            field=models.ImageField(default='Default_pfp.svg', upload_to='profile_images'),
        ),
    ]
