# Generated by Django 2.2.14 on 2020-08-03 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminstration', '0004_auto_20200802_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comittee',
            name='manager',
        ),
    ]
