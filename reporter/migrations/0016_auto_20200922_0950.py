# Generated by Django 3.1.1 on 2020-09-22 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporter', '0015_auto_20200917_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informationlist',
            name='department',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='report',
            name='department',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]