# Generated by Django 2.2.14 on 2020-08-22 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_management', '0025_voter_has_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='has_identifier',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
