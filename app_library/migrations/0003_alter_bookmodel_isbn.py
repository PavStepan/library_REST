# Generated by Django 4.1.2 on 2022-11-01 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_library', '0002_rename_name_bookmodel_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmodel',
            name='isbn',
            field=models.CharField(max_length=6, unique=True),
        ),
    ]
