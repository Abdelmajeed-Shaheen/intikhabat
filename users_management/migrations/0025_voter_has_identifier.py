# Generated by Django 2.2.14 on 2020-08-22 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_management', '0024_auto_20200819_0751'),
    ]

    operations = [
        migrations.AddField(
            model_name='voter',
            name='has_identifier',
            field=models.BooleanField(default=False),
        ),
    ]
