# Generated by Django 2.2.14 on 2020-09-06 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminstration', '0010_auto_20200828_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='comittee',
            name='communication_comittee',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comittee',
            name='election_box_comittee',
            field=models.BooleanField(default=False),
        ),
    ]
