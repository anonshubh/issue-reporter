# Generated by Django 3.1.1 on 2020-10-15 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('infolist', '0002_auto_20201015_0958'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='infolist',
            options={'ordering': ['-timestamp']},
        ),
    ]