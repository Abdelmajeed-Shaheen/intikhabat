# Generated by Django 2.2.14 on 2020-08-27 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminstration', '0008_auto_20200816_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='comittee',
            name='address_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]