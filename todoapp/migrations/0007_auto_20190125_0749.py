# Generated by Django 2.1.5 on 2019-01-25 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0006_auto_20190125_0659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemodel',
            name='mediaFile',
            field=models.FileField(null=True, upload_to='uploadedFiles/'),
        ),
    ]
