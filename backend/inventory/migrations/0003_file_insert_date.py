# Generated by Django 4.1 on 2022-12-13 12:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_file_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='insert_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]