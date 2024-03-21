# Generated by Django 4.2.11 on 2024-03-20 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formula', '0004_customuser_bio_customuser_is_admin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(max_length=4096),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='bio',
            field=models.TextField(blank=True, max_length=4096),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.CharField(max_length=4096),
        ),
        migrations.AlterField(
            model_name='team',
            name='description',
            field=models.CharField(max_length=4096),
        ),
        migrations.AlterField(
            model_name='topic',
            name='description',
            field=models.TextField(max_length=4096),
        ),
    ]
