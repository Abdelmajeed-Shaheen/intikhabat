# Generated by Django 2.2.14 on 2020-08-22 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_management', '0026_auto_20200822_0810'),
    ]

    operations = [
        migrations.AddField(
            model_name='voter',
            name='first_login',
            field=models.BooleanField(default=0),
        ),
    ]
